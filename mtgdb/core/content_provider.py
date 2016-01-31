import requests
import requests.exceptions
import zipfile
import io
import json
import os
import os.path

import mtgdb.exceptions
from mtgdb.core.data_labels import SET_LABELS


class ContentAvailability(object):
    """ Class that knows which content is available 'officially', and can give a differentiating
    view between official _availability and local _availability, as well as what content can be
    provided by the different content providers.
    """

    def __init__(self):
        self.official_content = MtgjsonContent()
        self.content_providers = [
            MtgjsonContent,
        ]

    def available_sets(self, remote=False):
        """
        Return a list of all the available official sets of mtg.
        :param remote: Allows the next call for data to go fetch the data remotely, if
        required.
        :return: A list of all the available sets with some extra information about
            each element.
        """
        sets = self.official_content.available_sets(remote=remote)
        return sets

    def populate(self, sets, data, remote=False):
        """
        Add additional information to the set dictionary. The data array specifies which
        information to add.
        :param sets: the original dictionary that needs to be populated with extra information
        :param data: data_id's for the type of data to add to the set dictionary
        :param remote: Allows the next call for data to go fetch the data remotely,
        if required.
        """
        for t_content_provider in self.content_providers:
            content_provider = t_content_provider()
            content_provider.populate(sets, data, remote=remote)


class MtgjsonContent(object):
    """
    Access the content available on http://mtgjson.com. This website publishes available
    mtg content in the form of json files containing all the information.
    """

    _ID_ALLSETS_X = 1

    _translation_table = {
        # codes
        SET_LABELS.CODE: 'code',
        SET_LABELS.GATHERER_CODE: 'gathererCode',
        SET_LABELS.OLD_CODE: 'oldCode',
        SET_LABELS.MCI_CODE: 'magicCardsInfoCode',

        # release info
        SET_LABELS.RELEASE_DATE: 'releaseDate',
        SET_LABELS.LANGUAGES: 'languagesPrinted',
        SET_LABELS.ONLINE_ONLY: 'onlineOnly',

        # general info
        SET_LABELS.BLOCK: 'block',
        SET_LABELS.NAME: 'name',
        SET_LABELS.CARDS: 'cards',
        SET_LABELS.NR_CARDS: None,
        SET_LABELS.TYPE: 'type',

        # special
        SET_LABELS.BORDER: 'border',
        SET_LABELS.BOOSTER: 'booster',
    }

    def __init__(self):
        self._data = {}
        self._next_call_remote = {
            self._ID_ALLSETS_X: False,
        }
        self._label_translation_table = None

    def _url_location(self, data_file_id):
        """
        Returns a URL location depending on the data the user wishes to access\n
        :param data_file_id: ID of the data. Starts with _ID\n
        :return: The URL pointing to the requested data, or none if the ID is invalid\n
        """
        _URL_BASE = "http://mtgjson.com/"
        _URL_ALLSETS_ZIP = "json/AllSets-x.json.zip"

        selector = {
            self._ID_ALLSETS_X: _URL_BASE + _URL_ALLSETS_ZIP
        }
        return selector.get(data_file_id)

    def _data_location(self, data_file_id):
        """
        Returns a folder location depending on the data the user wishes to access.\n
        :param data_file_id: ID Of the data, starts with _ID\n
        :return: A path to the requested data, or None if the ID is invalid.\n
        """
        _DATA_BASE = "data"
        _DATA_ALLSETS = "allsets.json"

        selector = {
            self._ID_ALLSETS_X: _DATA_BASE + os.sep + _DATA_ALLSETS
        }
        return selector.get(data_file_id)

    def _get_data_local(self, data_file_id):
        """
        Attempt to get the requested data from local storage.\n
        :param data_file_id: identifier specifying which data is being requested.\n
        :return: the file handle for the data, if the file existed locally. None if
        the file did not exist.\n
        """
        data_path = self._data_location(data_file_id)
        if os.path.isfile(data_path):
            return open(data_path)
        return None

    def _get_data_remote(self, data_file_id):
        """
        Attempt to get the requested data from a remote location.\n
        :param data_file_id: identifier specifying which data is being requested.\n
        :return: the file handle for the data, if the file could be retrieved successfully.
        Otherwise an exception is thrown.\n
        :raises: \n
            \tzipfile.BadZipFile: thrown if retrieved archive could not be opened.\n
            \trequests.exceptions.ConnectionError: thrown if there was an issue connecting
            to the remote data provider.\n
        """
        try:
            # get the allsets json file from mtgjson & unzip it.
            allsets_zipped = requests.get(self._url_location(data_file_id))
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

    def _save_data_local(self, data_file_id):
        """
        Save the data locally for future reference.\n
        :param data_file_id: identifier for the data, determines how the data will be saved.\n
        The data will be fetched from the internal memory of the class.\n
        """
        data_path = self._data_location(data_file_id)
        with open(data_path, 'w') as output_json:
            json.dump(self._data[data_file_id], output_json, indent=4)

    def _get_data(self, data_file_id, remote=False):
        """
        Get the data with given data_file_id. This data might be opened from local
        stores or from the internet.
        :param data_file_id: identifier for the data, determines the data that is requested.
        :param remote: specifies whether the data may be retrieved remotely if it
        is not available locally. Preference will always be given to the locally cached data
        if available. If the data is not available locally and get_remote is false, a
        DataUnavailable exception will be raised.
        :return: json object containing the data.
        :raises DataUnavailable: raised when the data is not locally available but the
        get_remote flag is set to false
        """
        if self._data.get(data_file_id, None) is not None:
            return self._data[data_file_id]

        # If for some reason the next call should always be allowed
        # remote access, then it is forced here. This might be the
        # case after a cache clear for example.
        if self._next_call_remote[data_file_id]:
            remote = True

        allsets_file = self._get_data_local(data_file_id)

        if allsets_file is not None:
            allsets_available_locally = True
        elif not remote:
            raise mtgdb.exceptions.DataUnavailable(
                "Requested data [{}] unavailable locally. ".format(self._data_location(data_file_id)) +
                "Need permission to fetch remotely")
        else:
            try:
                allsets_file = self._get_data_remote(data_file_id)
                allsets_available_locally = False

            except requests.exceptions.ConnectionError:
                import sys
                raise mtgdb.exceptions.DataUnavailable, \
                    mtgdb.exceptions.DataUnavailable("[ConnectionError]" +
                                                     "Could not retrieve remote resource."), \
                    sys.exc_info()[2]

        try:
            self._data[data_file_id] = json.load(allsets_file)
            # Save locally for future reference if it wasn't local yet.
            if not allsets_available_locally:
                self._save_data_local(data_file_id)

        except ValueError as vex:
            # json could not be processed
            import sys

            raise mtgdb.exceptions.InvalidDataError, \
                mtgdb.exceptions.InvalidDataError("Invalid data for json: " + vex.args[0]), \
                sys.exc_info()[2]

        finally:
            if allsets_file is not None:
                allsets_file.close()

        return self._data[data_file_id]

    def clear_cache(self):
        """
        Clears the cache of the MtgJsonContentProvider. The data will
        have to be downloaded again.
        NOTE: this forces the next call to data to be forced to go remote.
        NOTE_2: TODO: The requirement to go remote should be remembered between
        closing and starting the application.
        """
        self._data = {}
        # Force remote for each subsequent call to a new data_item.
        for data_key in self._next_call_remote:
            self._next_call_remote[data_key] = True

        # remove files.
        file_path = self._data_location(self._ID_ALLSETS_X)
        os.remove(file_path)

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
        return [{SET_LABELS.NAME: allsets_json[set_code]["name"],
                 SET_LABELS.CODE: allsets_json[set_code]["code"]} for set_code in allsets_json]

    def populate(self, sets, data_labels, remote=False):
        """
        Add additional information to the set dictionary. The data array specifies which
        information to add.

        Only the data that is available here will be added to the dictionary.

        :param sets: the original list of set dictionaries that needs to be populated
        with extra information
        :param data_labels: labels of the type of data to add to the dictionary
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

        if not data_labels:
            # No data needs to be added.
            return sets

        for mtgset in sets:
            code = mtgset[SET_LABELS.CODE]

            self._populate_code_information(allsets_json, code, data_labels, mtgset)
            self._populate_online_info(allsets_json, code, data_labels, mtgset)

            if SET_LABELS.NR_CARDS in data_labels:
                self._populate_nr_cards(allsets_json, code, mtgset)

            #
            # Copy over values of all the other attributes
            #
            for set_label in data_labels:
                # skip data_labels not supported by mtgjson content provider
                translated_label = self._translate_label(self._ID_ALLSETS_X, set_label)
                if translated_label is None:
                    continue
                # skip data_labels that have already been set
                if mtgset.get(set_label) is None and allsets_json[code].get(translated_label) is not None:
                    mtgset[set_label] = allsets_json[code][translated_label]

    def _populate_nr_cards(self, allsets_json, code, mtgset):
        """
        Populate the mtgset with the nr of cards in the set.
        :param allsets_json: contains all the known information about all the sets
        :param code: code of the set under inspection
        :param mtgset: the set currently being populated
        """

        cards_label = self._translate_label(self._ID_ALLSETS_X, SET_LABELS.CARDS)
        if allsets_json[code].get(cards_label, None) is None:
            mtgset[SET_LABELS.NR_CARDS] = 0
        else:
            cards = allsets_json[code][cards_label]
            mtgset[SET_LABELS.NR_CARDS] = len(cards)

    def _populate_online_info(self, allsets_json, code, data_labels, mtgset):
        """
        Populate the information of whether a card is only online or not. This information
        is not always set in the allsets_json data, and therefore might need to be set
        according if it's not set yet.
        :param allsets_json: contains all the sets information that is available officially
        :param code: code of the set under inspection
        :param data_labels: labels of the information to populate
        :param mtgset: the set under inspection that gets populated.
        """
        #
        # Set onlineOnly attribute
        #
        if SET_LABELS.ONLINE_ONLY in data_labels and mtgset.get(SET_LABELS.ONLINE_ONLY) is None:
            # If it's not set, ONLINE_ONLY = False
            translated_label = self._translate_label(self._ID_ALLSETS_X, SET_LABELS.ONLINE_ONLY)
            if allsets_json[code].get(translated_label) is not None:
                mtgset[SET_LABELS.ONLINE_ONLY] = allsets_json[code][translated_label]
            else:
                mtgset[SET_LABELS.ONLINE_ONLY] = False

    def _populate_code_information(self, allsets_json, code, data_labels, mtgset):
        """
        Populate the set code information. Some codes might not have been set in the official
        data in which case the code values follow certain rules. This method follows those
        rules and sets code information for set codes that are not set in the official data.

        :param allsets_json: contains all the sets information that is available officially
        :param code: code of the set under inspection
        :param data_labels: labels of the information to populate
        :param mtgset: the set under inspection that gets populated.
        """
        #
        # Populate code information
        #
        if SET_LABELS.GATHERER_CODE in data_labels and \
                mtgset.get(SET_LABELS.GATHERER_CODE) is None:

            # If GATHERER_CODE is not set, the code is identical to CODE
            translated_label = self._translate_label(self._ID_ALLSETS_X, SET_LABELS.GATHERER_CODE)
            if allsets_json[code].get(translated_label) is not None:
                mtgset[SET_LABELS.GATHERER_CODE] = allsets_json[code][translated_label]
            else:
                mtgset[SET_LABELS.GATHERER_CODE] = mtgset[SET_LABELS.CODE]

        if SET_LABELS.OLD_CODE in data_labels and \
                mtgset.get(SET_LABELS.OLD_CODE) is None:

            # Only set if OLD_CODE != GATHERER_CODE OR OLD_CODE != CODE
            translated_label = self._translate_label(self._ID_ALLSETS_X, SET_LABELS.OLD_CODE)
            if allsets_json[code].get(translated_label) is not None:
                mtgset[SET_LABELS.OLD_CODE] = allsets_json[code][translated_label]
            else:
                mtgset[SET_LABELS.OLD_CODE] = mtgset[SET_LABELS.CODE]

        if SET_LABELS.MCI_CODE in data_labels and \
                mtgset.get(SET_LABELS.MCI_CODE) is None:

            # Only set if magicCards.info has this set.
            translated_label = self._translate_label(self._ID_ALLSETS_X, SET_LABELS.MCI_CODE)
            if allsets_json[code].get(translated_label) is not None:
                mtgset[SET_LABELS.MCI_CODE] = allsets_json[code][translated_label]

    #
    # Label translation region
    #

    def _translate_label(self, data_id, set_label):
        """
        Translates a given 'set_label' to the label
        that is used for that information by the current
        mtgjson content provider, for data of given type (data_id)
        :param data_id: Specifies the type of data the label is from.
        :param set_label: The label used by the SET_LABEL.
        :return: The label that gets used by the mtgjson content provider
        for the data corresponding to given set_label
        """
        if self._label_translation_table is None:
            self._label_translation_table = {
                self._ID_ALLSETS_X: self._translate_label_allsets_x,
            }

        assert data_id in self._label_translation_table, \
            "unknown data_id specified for label translation"

        translation_function = self._label_translation_table[data_id]
        return translation_function(set_label)

    def _translate_label_allsets_x(self, set_label):
        """
        Translate a set_label to the ALLSETS_X data labels.
        :param set_label: The label for the data in the SET_LABEL class. The label
        must have an existing counterpart in the translation table for these labels.
        :return: The label for the data in the ALLSETS_X data.
        """
        if set_label not in self._translation_table:
            return None
        return self._translation_table[set_label]
