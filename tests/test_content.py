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

        sets = self.content.available_sets()

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
        # self.content._get_data_local = mock.MagicMock()
        # self.content._get_data_local.return_value = mtgjson_data.data_file(mtgjson_data.data)
        self.content._get_data_remote = mock.MagicMock()
        self.content._save_data_local = mock.MagicMock()

        # TODO: TESTING MY MOCKING FUNCTION
        my_mock = my_mock_open(read_data=mtgjson_data.data)
        my_mock.side_effect = open_side_effect
        with mock.patch('__builtin__.open', new=my_mock) as patch:
        # Fake existence of the data on local storage so that
        # no requests to the internet are made if the file is present.
        # Mock out the open() function.
            sets = self.content.available_sets()
            from pprint import pprint

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
            self.assertRaises(mtgdb.exceptions.InvalidDataError, self.content.available_sets)

    def test_shouldReturnExceptionIfTheZipCannotBeReadFromInternet(self):
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = None

        with mock.patch('mtgdb.core.content_provider.requests.get') as get:
            get.return_value.content = mtgjson_data.faulty_zipped()
            self.assertRaises(mtgdb.exceptions.InvalidDataError, self.content.available_sets)

    def test_shouldReturnExceptionIfCantAccessInternet(self):
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = None

        with mock.patch('mtgdb.core.content_provider.requests.get') as get:
            get.side_effect = requests.exceptions.ConnectionError
            self.assertRaises(requests.exceptions.ConnectionError, self.content.available_sets)

    def test_shouldPopulateSetsWithAvailableInformation(self):
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = mtgjson_data.data_file()
        # CASE 1
        data_ids = [
            d_ids.SET_DATA.RELEASE_DATE
        ]
        sets = self.content.available_sets()
        self.assertDictEqual(sets, mtgjson_data.data_sets([d_ids.SET_DATA.RELEASE_DATE]),
                             "case 1: populating set list with release dates not succesful")

        # CASE 2
        data_ids = [
            d_ids.SET_DATA.BORDER
        ]
        sets = self.content.available_sets()
        self.assertDictEqual(sets, mtgjson_data.data_sets([d_ids.SET_DATA.BORDER]),
                             "case 2: populating set list with borders not succesful")

        # CASE 3
        data_ids = [
            d_ids.SET_DATA.BLOCK
        ]
        sets = self.content.available_sets()
        self.assertDictEqual(sets, mtgjson_data.data_sets([d_ids.SET_DATA.BLOCK]),
                             "case 3: populating set list with block not succesful")

        # CASE 4
        data_ids = [
            d_ids.SET_DATA.TYPE
        ]
        sets = self.content.available_sets()
        self.assertDictEqual(sets, mtgjson_data.data_sets([d_ids.SET_DATA.TYPE]),
                             "case 4: populating set list with set type not succesful")

        # CASE 5
        data_ids = [
            d_ids.SET_DATA.BOOSTER
        ]
        sets = self.content.available_sets()
        self.assertDictEqual(sets, mtgjson_data.data_sets([d_ids.SET_DATA.BOOSTER]),
                             "case 4: populating set list with boosters not succesful")


    def test_populateShouldIgnoreDataIdsThatAreNotAvailableByMtgjson(self):
        self.assertTrue(False, "Not Implemented Yet")


    def test_populatingWhenTheRequestedDataIsAlreadyAvailableDoesNothing(self):
        self.assertTrue(False, "Not Implemented Yet")

    def test_populateIsAnIdempotentMethod(self):
        self.assertTrue(False, "Not Implemented Yet")


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