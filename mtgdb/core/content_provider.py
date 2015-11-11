import requests, requests.exceptions
import zipfile
import io
import json
import os, os.path

import mtgdb.exceptions
from mtgdb.core.data_id import SET_DATA as SDID


class ContentAvailability(object):
    """ Class that knows which content is available 'officially', and can give a differentiating
    view between official availability and local availability, as well as what content can be
    provided by the different content providers.
    """

    def __init__(self):
        self.official_content = MtgjsonContent()
        self.content_providers = [
            MtgjsonContent,
        ]

    def available_sets(self):
        """
        Return a list of all the available official sets of mtg.
        :return: A list of all the available sets with some extra information about
            each element.
        """
        sets = self.official_content.available_sets()
        return sets

    def populate(self, sets, data):
        """
        Add additional information to the set dictionary. The data array specifies which
        information to add.
        :param sets: the original dictionary that needs to be populated with extra information
        :param data: data_id's for the type of data to add to the set dictionary
        """
        for content_provider_t in self.content_providers:
            content_provider = content_provider_t()
            content_provider.populate(sets, data)


class MtgjsonContent(object):
    """
    Access the content available on http://mtgjson.com. This website publishes available
    mtg content in the form of json files containing all the information.
    """

    _ID_ALLSETS_X = 1

    _data_id = {
        # codes
        SDID.CODE: 'code',
        SDID.GATHERER_CODE: 'gathererCode',
        SDID.OLD_CODE: 'oldCode',
        SDID.MCI_CODE: 'magicCardsInfoCode',

        # release info
        SDID.RELEASE_DATE: 'releaseDate',
        SDID.LANGUAGES: 'languagesPrinted',
        SDID.ONLINE_ONLY: 'onlineOnly',

        # general info
        SDID.BLOCK: 'block',
        SDID.NAME: 'name',
        SDID.CARDS: 'cards',
        SDID.TYPE: 'type',

        # special
        SDID.BORDER: 'border',
        SDID.BOOSTER: 'booster',
    }

    def __init__(self):
        self._data = {}

    def _url_location(self, data_id):
        """
        Returns a URL location depending on the data the user wishes to access\n
        :param data_id: ID of the data. Starts with _ID\n
        :return: The URL pointing to the requested data, or none if the ID is invalid\n
        """
        _URL_BASE = "http://mtgjson.com/"
        _URL_ALLSETS_ZIP = "json/AllSets-x.json.zip"

        selector = {
            self._ID_ALLSETS_X: _URL_BASE + _URL_ALLSETS_ZIP
        }
        return selector.get(data_id)

    def _data_location(self, data_id):
        """
        Returns a folder location depending on the data the user wishes to access.\n
        :param data_id: ID Of the data, starts with _ID\n
        :return: A path to the requested data, or None if the ID is invalid.\n
        """
        _DATA_BASE = "data"
        _DATA_ALLSETS = "allsets.json"

        selector = {
            self._ID_ALLSETS_X: _DATA_BASE + os.sep + _DATA_ALLSETS
        }
        return selector.get(data_id)

    def _get_data_local(self, data_id):
        """
        Attempt to get the requested data from local storage.\n
        :param data_id: identifier specifying which data is being requested.\n
        :return: the file handle for the data, if the file existed locally. None if
        the file did not exist.\n
        """
        if os.path.isfile(self._data_location(data_id)):
            return open(self._data_location(self._ID_ALLSETS_X), 'r')
        return None

    def _get_data_remote(self, data_id):
        """
        Attempt to get the requested data from a remote location.\n
        :param data_id: identifier specifying which data is being requested.\n
        :return: the file handle for the data, if the file could be retrieved successfully.
        Otherwise an exception is thrown.\n
        :raises: \n
            \tzipfile.BadZipFile: thrown if retrieved archive could not be opened.\n
            \trequests.exceptions.ConnectionError: thrown if there was an issue connecting
            to the remote data provider.\n
        """
        try:
            # get the allsets json file from mtgjson & unzip it.
            allsets_zipped = requests.get(self._url_location(data_id))
            allsets_zipfile = zipfile.ZipFile(io.BytesIO(allsets_zipped.content))
            allsets_zipinfo = allsets_zipfile.infolist()
            allsets_file = allsets_zipfile.open(allsets_zipinfo[0], 'rU')
            allsets_zipfile.close()
            return allsets_file

        except zipfile.BadZipfile as zipex:
            import sys

            raise mtgdb.exceptions.InvalidDataError, \
                mtgdb.exceptions.InvalidDataError("Invalid zip file: " + zipex.args[0]), \
                sys.exc_info()[2]

        except requests.exceptions.ConnectionError as cerr:
            import sys

            raise requests.exceptions.ConnectionError, \
                requests.exceptions.ConnectionError("Error downloading file: " + cerr.message), \
                sys.exc_info()[2]

    def _save_data_local(self, data_id):
        """
        Save the data locally for future reference.\n
        :param data_id: identifier for the data, determines how the data will be saved.\n
        The data will be fetched from the internal memory of the class.\n
        """
        with open(self._data_location(data_id), 'w') as output_json:
            json.dump(self._data[data_id], output_json, indent=4)

    def _get_data(self, data_id, get_remote=False):
        """
        Get the data with given data_id. This data might be opened from local
        stores or from the internet.
        :param data_id: identifier for the data, determines the data that is requested.
        :param get_remote: specifies whether the data may be retrieved remotely if it
        is not available locally. Preference will always be given to the locally cached data
        if available. If the data is not available locally and get_remote is false, a
        DataUnavailable exception will be raised.
        :return: json object containing the data.
        :raises DataUnavailable: raised when the data is not locally available but the
        get_remote flag is set to false
        """
        if self._data.get(data_id, None) is not None:
            return self._data[data_id]

        allsets_file = self._get_data_local(data_id)

        if allsets_file is not None:
            allsets_available_locally = True
        elif not get_remote:
            raise mtgdb.exceptions.DataUnavailable(
                "Requested data [{}] unavailable locally. ".format(self._data_location(data_id)) +
                "Need permission to fetch remotely")
        else:
            try:
                allsets_file = self._get_data_remote(data_id)
                allsets_available_locally = False

            except requests.exceptions.ConnectionError:
                import sys
                raise mtgdb.exceptions.DataUnavailable, \
                    mtgdb.exceptions.DataUnavailable("[ConnectionError]" +
                                                     "Could not retrieve remote resource."), \
                    sys.exc_info()[2]

        try:
            self._data[data_id] = json.load(allsets_file)
            # Save locally for future reference if it wasn't local yet.
            if not allsets_available_locally:
                self._save_data_local(data_id)

        except ValueError as vex:
            # json could not be processed
            import sys

            raise mtgdb.exceptions.InvalidDataError, \
                mtgdb.exceptions.InvalidDataError("Invalid data for json: " + vex.args[0]), \
                sys.exc_info()[2]

        finally:
            if allsets_file is not None:
                allsets_file.close()

        return self._data[data_id]

    def available_sets(self, remote=False):
        """
        Returns a list of all the sets that are available on mtgjson. If the data is not
        locally available it may be retrieved from a remote provider and cached locally for
        future reference.\n
        :param remote: specifies whether the data may be retrieved remotely if it
        is not available locally. Preference will always be given to the locally cached data
        if available. If the data is not available locally and remote is false, a
        DataUnavailable exception will be raised.
        :return: a list of all the sets that are available on mtgjson.\n
        :raises:\n
            \t-mtgdb.exceptions.InvalidDataError: thrown if the data was could not be accessed
            because it was either corrupt.\n
            \tmtgdb.exceptions.DataUnavailable: raised when the data was not available. This could
            be not available locally with remote flag=False or remote flag=True but not being able
            to connect to the remote resource.
        """
        allsets_json = self._get_data(self._ID_ALLSETS_X, remote)

        # read sets from json data.
        return [{SDID.NAME: allsets_json[set_code]["name"],
                 SDID.CODE: allsets_json[set_code]["code"]} for set_code in allsets_json]

    def populate(self, sets, data_ids, remote=False):
        """
        Add additional information to the set dictionary. The data array specifies which
        information to add.

        Only the data that is available here will be added to the dictionary.

        :param sets: the original list of set dictionaries that needs to be populated
        with extra information
        :param data_ids: data_id's for the type of data to add to the set dictionary
        :param remote: specifies whether the data may be retrieved remotely if it
        is not available locally. Preference will always be given to the locally cached data
        if available. If the data is not available locally and remote is false, a
        DataUnavailable exception will be raised.
        :raises:\n
            \t-mtgdb.exceptions.InvalidDataError: thrown if the data was could not be accessed
            because it was either corrupt.\n
            \tmtgdb.exceptions.DataUnavailable: raised when the data was not available. This could
            be not available locally with remote flag=False or remote flag=True but not being able
            to connect to the remote resource.
        """
        allsets_json = self._get_data(self._ID_ALLSETS_X, remote)

        if not data_ids:
            # No data needs to be added.
            return sets

        for set in sets:
            code = set[SDID.CODE]

            # Populate code information
            if SDID.GATHERER_CODE in data_ids and set.get(SDID.GATHERER_CODE) is None:
                # If GATHERER_CODE is not set, the code is identical to CODE
                if allsets_json[code].get(self._data_id[SDID.GATHERER_CODE]) is not None:
                    set[SDID.GATHERER_CODE] = allsets_json[code][self._data_id[SDID.GATHERER_CODE]]
                else:
                    set[SDID.GATHERER_CODE] = set[SDID.CODE]

            if SDID.OLD_CODE in data_ids and set.get(SDID.OLD_CODE) is None:
                # Only set if OLD_CODE != GATHERER_CODE OR OLD_CODE != CODE
                if allsets_json[code].get(self._data_id[SDID.OLD_CODE]) is not None:
                    set[SDID.OLD_CODE] = allsets_json[code][self._data_id[SDID.OLD_CODE]]
                else:
                    set[SDID.OLD_CODE] = set[SDID.CODE]

            if SDID.MCI_CODE in data_ids and set.get(SDID.MCI_CODE) is None:
                # Only set if magicCards.info has this set.
                if allsets_json[code].get(self._data_id[SDID.MCI_CODE]) is not None:
                    set[SDID.MCI_CODE] = allsets_json[code][self._data_id[SDID.MCI_CODE]]

            # Set onlineOnly attribute
            if SDID.ONLINE_ONLY in data_ids and set.get(SDID.ONLINE_ONLY) is None:
                # If it's not set, ONLINE_ONLY = False
                if allsets_json[code].get(self._data_id[SDID.ONLINE_ONLY]) is not None:
                    set[SDID.ONLINE_ONLY] = allsets_json[code][self._data_id[SDID.ONLINE_ONLY]]
                else:
                    set[SDID.ONLINE_ONLY] = False

            # Copy over values of all the other attributes
            for data_id in data_ids:
                # skip data_ids not supported by mtgjson content provider
                if self._data_id.get(data_id) is None:
                    continue
                # skip data_ids that have already been set
                if set.get(data_id) is None and allsets_json[code].get(self._data_id[data_id]) is not None:
                    set[data_id] = allsets_json[code][self._data_id[data_id]]
