import content_provider

class DataView(object):

    def __init__(self):
        self.availability = content_provider.ContentAvailability()

    def available_sets(self, data=[]):
        """
        Returns available sets with all the available, requested data.


        :param data: data_id.SET_DATA identifiers for any additional information
            wanted about sets.
        :return: returns all the available information requested, for all the official sets.
            SET_DATA.CODE, and SET_DATA.NAME are included in the information by default.
        """
        sets = self.availability.available_sets()

        return sets
