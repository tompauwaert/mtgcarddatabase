import unittest
import json

import mock
import requests.exceptions
import mtgdb.core.content_provider
import mtgdb.exceptions
import tests.data.mtgjson_testdata as mtgjson_data
import mtgdb.core.data_id as d_ids


class ContentAvailabilityTest(unittest.TestCase):

    def setUp(self):
        self.availability = mtgdb.core.content_provider.ContentAvailability()

    # @mock.patch('mtgdb.core.content_provider.MtgjsonContent.available_sets',
    #             return_value=mtgjson_data.data_sets())
    def test_shouldReturnListOfAllOfficialyAvailableSets(self):
        with mock.patch('mtgdb.core.content_provider.MtgjsonContent.available_sets') as m_mtg:
            m_mtg.return_value = mtgjson_data.data_sets()
            self.assertListEqual(self.availability.available_sets(), mtgjson_data.data_sets())


class MtgjsonContentTest(unittest.TestCase):

    def setUp(self):
        self.content = mtgdb.core.content_provider.MtgjsonContent()

    # noinspection PyUnresolvedReferences
    def test_shouldReturnListOfAllAvailableSetsFromInternetLast(self):
        # mock returns zipped test-data json.
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = None
        self.content._get_data_remote = mock.MagicMock()
        self.content._get_data_remote.return_value = mtgjson_data.data_file(mtgjson_data.data)
        self.content._save_data_local = mock.MagicMock()

        sets = self.content.available_sets(remote=True)

        self.assertListEqual(sets, mtgjson_data.data_sets(),
                             "test returns incorrect list of available sets.")
        self.assertTrue(self.content._get_data_local.called,
                        "test did not check for local data first")
        self.assertTrue(self.content._get_data_remote.called,
                        "test did not check remote location for data")
        self.assertTrue(self.content._save_data_local.called_with_args(
                        self.content._ID_ALLSETS_X,
                        json.loads(mtgjson_data.data)),
                        "test did not try and save remote data locally")


    @mock.patch('mtgdb.core.content_provider.os.path.isfile', return_value=True)
    def test_shouldReturnListOfAllAvailableSetsFromLocalStorageFirst(self, m_isfile) :
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = mtgjson_data.data_file(mtgjson_data.data)
        self.content._get_data_remote = mock.MagicMock()
        self.content._save_data_local = mock.MagicMock()

        # TODO: TESTING MY MOCKING FUNCTION
        # my_mock = my_mock_open(read_data=mtgjson_data.data)
        # my_mock.side_effect = open_side_effect
        # with mock.patch('__builtin__.open', new=my_mock) as patch:
        # Fake existence of the data on local storage so that
        # no requests to the internet are made if the file is present.
        # Mock out the open() function.
        sets = self.content.available_sets()
            # from pprint import pprint

        self.assertListEqual(sets, mtgjson_data.data_sets(),
                             "Test returns incorrect list of available sets.")
        # at least one call to open must have tried reading the set data locally
        # self.assertTrue(self.content._get_data_local.called,
        #                 'should get the data locally first.')
        self.assertFalse(self.content._get_data_remote.called,
                         'should not attempt to request from internet.')
        self.assertFalse(self.content._save_data_local.called,
                         'should not attempt to save to local storage, it already exists')

    def test_shouldReturnExceptionIfTheJsonReceivedFromInternetIsInvalid(self):
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = None

        with mock.patch('mtgdb.core.content_provider.requests.get') as get:
            get.return_value.content = \
                mtgjson_data.data_zipped(mtgjson_data.data_malformed_json)
            self.assertRaises(mtgdb.exceptions.InvalidDataError,
                              self.content.available_sets,
                              True)

    def test_shouldReturnExceptionIfTheZipCannotBeReadFromInternet(self):
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = None

        with mock.patch('mtgdb.core.content_provider.requests.get') as get:
            get.return_value.content = mtgjson_data.faulty_zipped()
            self.assertRaises(mtgdb.exceptions.InvalidDataError,
                              self.content.available_sets,
                              True)

    def test_shouldReturnExceptionIfCantAccessInternet(self):
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = None

        with mock.patch('mtgdb.core.content_provider.requests.get') as get:
            get.side_effect = requests.exceptions.ConnectionError
            self.assertRaises(mtgdb.exceptions.DataUnavailable,
                              self.content.available_sets,
                              True)

    def test_populateShouldAddAvailableInformationToSets(self):
        self.content._get_data_local = mock.MagicMock()

        # CASE 1
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.RELEASE_DATE]),
                             "case 1: populating set list with release dates not successful")

        # CASE 2
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.BORDER
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                             [d_ids.SET_DATA.BORDER]),
                             "case 2: populating set list with borders not successful")

        # CASE 3
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.BLOCK
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.BLOCK]),
                             "case 3: populating set list with block not successful")

        # CASE 4
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.TYPE
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.TYPE]),
                             "case 4: populating set list with set type not successful")

        # CASE 5
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.BOOSTER
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.BOOSTER]),
                             "case 5: populating set list with boosters not successful")

        # CASE 6
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.OLD_CODE
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.OLD_CODE]),
                             "case 6: populating set list with old_code not successful")

        # CASE 7
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.MCI_CODE
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.MCI_CODE]),
                             "case 7: populating set list with mci_code not successful")

        # CASE 8
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.GATHERER_CODE
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.GATHERER_CODE]),
                             "case 8: populating set list with gatherer_code not successful")

        # CASE 9
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.ONLINE_ONLY
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.ONLINE_ONLY]),
                             "case 9: populating set list with online_only not successful")

        # CASE 10
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.BLOCK,
            d_ids.SET_DATA.TYPE,
            d_ids.SET_DATA.RELEASE_DATE,
            d_ids.SET_DATA.GATHERER_CODE
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [
                                                              d_ids.SET_DATA.BLOCK,
                                                              d_ids.SET_DATA.TYPE,
                                                              d_ids.SET_DATA.RELEASE_DATE,
                                                              d_ids.SET_DATA.GATHERER_CODE
                                                          ]),
                             "case 10: populating set list with multiple fields not successful")

    def test_populateShouldIgnoreDataIdsThatAreNotAvailableByMtgjson(self):
        self.content._get_data_local = mock.MagicMock()

        # CASE 1
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            'does_not_exist',
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(data=mtgjson_data.data_extended),
                             "case 1: does not correctly handle non-available labels")

        # CASE 2
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE,
            'does_not_exist',
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [d_ids.SET_DATA.RELEASE_DATE]),
                             "case 2: does not correctly handle non-available labels")

    def test_populatingWhenTheRequestedDataIsAlreadyAvailableDoesNothing(self):
        self.content._get_data_local = mock.MagicMock()

        # CASE 1
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE,
        ]
        sets = mtgjson_data.data_sets(mtgjson_data.data_extended, data_ids) #already contains 'release date'
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          d_ids.SET_DATA.RELEASE_DATE),
                             "case 1: wrong population behavior when is data already present")

        # CASE 2
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE,
            d_ids.SET_DATA.BORDER,
        ]
        sets = mtgjson_data.data_sets(mtgjson_data.data_extended, data_ids) #already contains 'release date'
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                          [
                                                              d_ids.SET_DATA.RELEASE_DATE,
                                                              d_ids.SET_DATA.BORDER,
                                                          ]),
                             "case 2: wrong population behavior when is data already present")

    def test_populateIsAnIdempotentMethod(self):
        self.content._get_data_local = mock.MagicMock()

        # CASE 1
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE,
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended, [
            d_ids.SET_DATA.RELEASE_DATE,
        ]),
                             "case 1: populate is not idempotent")

        # CASE 2
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE,
            d_ids.SET_DATA.BLOCK,
            d_ids.SET_DATA.TYPE,
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended, [
            d_ids.SET_DATA.RELEASE_DATE,
            d_ids.SET_DATA.BLOCK,
            d_ids.SET_DATA.TYPE,
        ]),
                             "case 2: populate is not idempotent")

        # CASE 3
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE,
            d_ids.SET_DATA.BLOCK,
            d_ids.SET_DATA.TYPE,
            'non_existant',
        ]
        sets = self.content.available_sets()
        self.content.populate(sets, data_ids)
        self.content.populate(sets, data_ids)
        self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended, [
            d_ids.SET_DATA.RELEASE_DATE,
            d_ids.SET_DATA.BLOCK,
            d_ids.SET_DATA.TYPE,
        ]),
                             "case 3: populate is not idempotent when introducing " +
                             "non-existant d_id")

    def test_TEST_GET_DATA_METHOD(self):
        self.assertTrue(False, "Not Implemented")



def open_side_effect(*arg, **kwargs):
    from pprint import pprint
    pprint(arg)

    handle = mock.MagicMock()
    handle.write.return_value = None
    handle.__enter__.return_value = handle
    # handle.read.return_value = read_data


def my_mock_open(m=None, read_data=''):
    if m is None:
        m = mock.MagicMock(name='open')

    handle = mock.MagicMock()
    handle.write.return_value = None
    handle.__enter__.return_value = handle
    handle.read.return_value = read_data

    m.return_value = handle
    return m

def suite():
    test_classes = [
        MtgjsonContentTest,
        ContentAvailabilityTest,
    ]
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    return suite

if __name__ == "__main__":
    unittest.main()