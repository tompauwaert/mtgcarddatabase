import unittest
import mock
import requests.exceptions
import json
import StringIO

import mtgdb.content_provider
import mtgdb.exceptions

import tests.data.mtgjson_testdata as mtgjson_data


class ContentAvailabilityTest(unittest.TestCase):
    pass
    # def test_shouldReturnListOfAllAvailableOfficialSets(self):
    #     availability = mtgdb.content_provider.ContentAvailability()
    #     sets = availability.available_sets()
    #     self.assertFalse(len(sets) == 0, "Set list 'available sets' is empty.")



class MtgjsonContentTest(unittest.TestCase):

    def setUp(self):
        self.content = mtgdb.content_provider.MtgjsonContent()
        self.mock_requests_response = mock.Mock()
        self.mock_requests_response.content = mtgjson_data.data_zipped()


    @mock.patch('mtgdb.content_provider.os.path.isfile', return_value=False)
    @mock.patch('mtgdb.content_provider.requests.get')
    @mock.patch('mtgdb.content_provider.json.dump')
    def test_shouldReturnListOfAllAvailableSetsFromInternetLast(self, m_dump, m_req, m_isfile):
        # mock returns zipped test-data json.
        self.mock_requests_response.reset_mock()
        m_req.return_value = self.mock_requests_response
        m_isfile.return_value = False

        with mock.patch('mtgdb.content_provider.open', mock.mock_open(),
                        create=True) as m_open:
            sets = self.content.available_sets()
            self.assertListEqual(sets, mtgjson_data.data_sets(),
                                 "Test returns incorrect list of available sets.")
            self.assertTrue(m_req.called)
            self.assertTrue(m_dump.called)
            self.assertTrue(m_open().write.called_with_args(mtgjson_data.data))


    @mock.patch('mtgdb.content_provider.requests.get')
    @mock.patch('mtgdb.content_provider.json.dump')
    @mock.patch('mtgdb.content_provider.os.path.isfile', return_value=True)
    def test_shouldReturnListOfAllAvailableSetsFromLocalStorageFirst(self, m_isfile,
                                                                     m_dump, m_req):
        self.mock_requests_response.reset_mock()
        m_req.return_value = self.mock_requests_response

        # Fake existence of the data on local storage so that
        # no requests to the internet are made if the file is present.
        # Mock out the open() function.
        with mock.patch('mtgdb.content_provider.open',
                        mock.mock_open(read_data=mtgjson_data.data),
                        create=True) as m_open:
            sets = self.content.available_sets()

            self.assertListEqual(sets, mtgjson_data.data_sets(),
                                 "Test returns incorrect list of available sets.")
            # at least one call to open must have tried reading the set data locally
            self.assertTrue(any(("r" in args[1] and "allsets" in args[0])
                            for args, kwargs in m_open.call_args_list),
                            "should have read from the local storage file")
            file_handle = m_open()
            self.assertTrue(file_handle.read.called)
            self.assertFalse(m_req.called, 'should not attempt to request from internet.')
            self.assertFalse(m_dump.called, 'should not attempt to save to local storage,' +
                                            'it already exists')

    @mock.patch('mtgdb.content_provider.os.path.isfile', return_value=False)
    @mock.patch('mtgdb.content_provider.requests.get')
    def test_shouldReturnExceptionIfTheJsonCannotBeReadFromInternet(self, m_req, m_isfile):
        m_req.return_value = mock.Mock()
        m_req.return_value.content = mtgjson_data.data_zipped(mtgjson_data.data_malformed_json)
        self.assertRaises(mtgdb.exceptions.InvalidDataError, self.content.available_sets)


    @mock.patch('mtgdb.content_provider.os.path.isfile', return_value=False)
    @mock.patch('mtgdb.content_provider.requests.get')
    def test_shouldReturnExceptionIfTheZipCannotBeReadFromInternet(self, m_req, m_isfile):
        m_req.return_value = mock.Mock()
        m_req.return_value.content = mtgjson_data.faulty_zipped()
        self.assertRaises(mtgdb.exceptions.InvalidDataError, self.content.available_sets)

    @mock.patch('mtgdb.content_provider.os.path.isfile', return_value=False)
    def test_shouldReturnExceptionIfCantAccessInternet(self, m_isfile):
        with mock.patch('mtgdb.content_provider.requests.get') as m_req:
            m_req.side_effect = requests.exceptions.ConnectionError
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