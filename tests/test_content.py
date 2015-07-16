import unittest
import json

import mock
import requests.exceptions
import mtgdb.core.content_provider
import mtgdb.exceptions
import tests.data.mtgjson_testdata as mtgjson_data


class ContentAvailabilityTest(unittest.TestCase):

    def setUp(self):
        self.availability = mtgdb.core.content_provider.ContentAvailability()

    @mock.patch('mtgdb.core.content_provider.MtgjsonContent.available_sets',
                return_value=mtgjson_data.data_sets())
    def test_shouldReturnListOfAllOfficialyAvailableSets(self, m_mtg):
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

    def test_shouldReturnListOfAllAvailableSetsFromLocalStorageFirst(self) :
        self.content._get_data_local = mock.MagicMock()
        self.content._get_data_local.return_value = mtgjson_data.data_file(mtgjson_data.data)
        self.content._get_data_remote = mock.MagicMock()
        self.content._save_data_local = mock.MagicMock()

        # Fake existence of the data on local storage so that
        # no requests to the internet are made if the file is present.
        # Mock out the open() function.
        sets = self.content.available_sets()

        self.assertListEqual(sets, mtgjson_data.data_sets(),
                             "Test returns incorrect list of available sets.")
        # at least one call to open must have tried reading the set data locally
        self.assertTrue(self.content._get_data_local.called,
                        'should get the data locally first.')
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