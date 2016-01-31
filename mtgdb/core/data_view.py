import content_provider
from data_labels import SET_LABELS

class DataView(object):

    def __init__(self):
        self._availability = content_provider.ContentAvailability()

    def available_sets(self, data=None, remote=False):
        """
        Returns available sets with all the available, requested data.

        :param data: data_labels.SET_DATA identifiers for any additional information
            wanted about sets.
        :param remote: Allows the next call for data to go fetch the data remotely, if required.
        :return: returns all the available information requested, for all the official sets.
            SET_DATA.CODE, SET_DATA.NAME, SET_DATA.RELEASE_DATE, and
            SET_DATA.BLOCK are included in the information by default.
        """
        if data is None:
            data = [SET_LABELS.RELEASE_DATE, SET_LABELS.BLOCK]
        else:
            if SET_LABELS.RELEASE_DATE not in data:
                data.append(SET_LABELS.RELEASE_DATE)
            if SET_LABELS.BLOCK not in data:
                data.append(SET_LABELS.BLOCK)

        sets = self._availability.available_sets(remote=remote)
        self._availability.populate(sets, data, remote=remote)

        return sets


