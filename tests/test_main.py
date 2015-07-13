import unittest
import mock
import requests.exceptions
import json
import StringIO

import mtgdb.content_provider
import mtgdb.exceptions

import tests.data.mtgjson_testdata as mtgjson_data


class ContentAvailabilityTest(unittest.TestCase):

    def setUp(self):
        self.availability = mtgdb.content_provider.ContentAvailability()

    def test_shouldReturnListOfAllOfficialyAvailableSets(self):
        pass


class MtgjsonContentTest(unittest.TestCase):

    def setUp(self):
        self.content = mtgdb.content_provider.MtgjsonContent()

    @mock.patch('mtgdb.content_provider.MtgjsonContent._get_data_local', return_value=None)
    @mock.patch('mtgdb.content_provider.MtgjsonContent._get_data_remote')
    @mock.patch('mtgdb.content_provider.MtgjsonContent._save_data_local')
    def test_shouldReturnListOfAllAvailableSetsFromInternetLast(self, m_save, m_remote, m_local):
        # mock returns zipped test-data json.
        m_remote.return_value = mtgjson_data.data_file(mtgjson_data.data)

        sets = self.content.available_sets()
        self.assertListEqual(sets, mtgjson_data.data_sets(),
                             "Test returns incorrect list of available sets.")
        self.assertTrue(m_remote.called)
        self.assertTrue(m_save.called_with_args(self.content._ID_ALLSETS_X,
                                                json.loads(mtgjson_data.data)))


    @mock.patch('mtgdb.content_provider.MtgjsonContent._get_data_local',
                return_value=mtgjson_data.data_file(mtgjson_data.data))
    @mock.patch('mtgdb.content_provider.MtgjsonContent._get_data_remote')
    @mock.patch('mtgdb.content_provider.MtgjsonContent._save_data_local')
    def test_shouldReturnListOfAllAvailableSetsFromLocalStorageFirst(self, m_local, m_remote, m_save) :
        m_remote.return_value = mtgjson_data.data_file(mtgjson_data.data)

        # Fake existence of the data on local storage so that
        # no requests to the internet are made if the file is present.
        # Mock out the open() function.
        sets = self.content.available_sets()

        self.assertListEqual(sets, mtgjson_data.data_sets(),
                             "Test returns incorrect list of available sets.")
        # at least one call to open must have tried reading the set data locally
        self.assertTrue(m_local.called)
        self.assertFalse(m_remote.called, 'should not attempt to request from internet.')
        self.assertFalse(m_save.called, 'should not attempt to save to local storage, it already exists')

    @mock.patch('mtgdb.content_provider.Mtgjsoncontent._get_data_local', return_value=None)
    @mock.patch('mtgdb.content_provider.Mtgjsoncontent._get_data_remote')
    def test_shouldReturnExceptionIfTheJsonCannotBeReadFromInternet(self, m_remote, m_local):
        m_remote.return_value = mtgjson_data.data_file(mtgjson_data.data_malformed_json)
        self.assertRaises(mtgdb.exceptions.InvalidDataError, self.content.available_sets)


    @mock.patch('mtgdb.content_provider.Mtgjsoncontent._get_data_local', return_value=None)
    @mock.patch('mtgdb.content_provider.requests.get')
    def test_shouldReturnExceptionIfTheZipCannotBeReadFromInternet(self, m_req, m_local):
        m_req.return_value = mock.MagicMock()
        m_req.return_value.content = mtgjson_data.faulty_zipped()
        self.assertRaises(mtgdb.exceptions.InvalidDataError, self.content.available_sets)

    @mock.patch('mtgdb.content_provider.Mtgjsoncontent._get_data_local', return_value=None)
    @mock.patch('mtgdb.content_provider.Mtgjsoncontent._get_data_remote',
                side_effect=requests.exceptions.ConnectionError)
    def test_shouldReturnExceptionIfCantAccessInternet(self, m_local):
        self.assertRaises(requests.exceptions.ConnectionError, self.content.available_sets)

def load_tests(loader, standard_tests, pattern):
    test_cases = [
        MtgjsonContentTest,
    ]
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == "__main__":
    unittest.main()