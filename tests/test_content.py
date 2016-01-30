import unittest
import json
import os

import mock
import requests.exceptions
import mtgdb.core.content_provider
import mtgdb.exceptions
import tests.data.mtgjson_testdata as mtgjson_data
import tests.test_utils
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
        self._path = "data" + os.sep + "allsets.json"
        self._url = "http://mtgjson.com/json/AllSets-x.json.zip"

    # noinspection PyUnresolvedReferences
    def test_shouldReturnListOfAllAvailableSetsFromInternetLast(self):
        with tests.test_utils.FileMocker() as f_mocker:
            f_mocker.register_file(self._path, False, "")

            with mock.patch('mtgdb.core.content_provider.requests.get') as get:
                get.return_value.content = mtgjson_data.data_zipped(mtgjson_data.data)

                sets = self.content.available_sets(remote=True)

                self.assertListEqual(sets, mtgjson_data.data_sets(),
                                     "test returns incorrect list of available sets.")
                self.assertTrue(f_mocker[self._path].file_exists_called(),
                                "test did not check for local data first")
                self.assertTrue(get.called,
                                "test did not check remote location for data")
                self.assertTrue(f_mocker[self._path].get_mock().write.called_with_args(
                                    self._path,
                                    json.loads(mtgjson_data.data)),
                                "test did not try and save remote data locally")

    def test_shouldReturnListOfAllAvailableSetsFromLocalStorageFirst(self):
        self.content._get_data_remote = mock.MagicMock()
        self.content._save_data_local = mock.MagicMock()

        with tests.test_utils.FileMocker() as f_mocker:
            f_mocker.register_file(self._path, True, mtgjson_data.data)

            sets = self.content.available_sets()
            self.assertListEqual(sets, mtgjson_data.data_sets(),
                                 "Test returns incorrect list of available sets.")
            # at least one call to open must have tried reading the set data locally
            file_mock = f_mocker[self._path]
            self.assertTrue(file_mock.get_mock().read.called,
                            'should get the data locally first.')
            self.assertFalse(self.content._get_data_remote.called,
                             'should not attempt to request from internet.')
            self.assertFalse(self.content._save_data_local.called,
                             'should not attempt to save to local storage, it already exists')

    def test_shouldReturnExceptionIfTheJsonReceivedFromInternetIsInvalid(self):
        with tests.test_utils.FileMocker() as f_mocker:
            # file does not exist locally
            f_mocker.register_file(self._path, False, "")

            with mock.patch('mtgdb.core.content_provider.requests.get') as get:
                get.return_value.content = \
                    mtgjson_data.data_zipped(mtgjson_data.data_malformed_json)
                self.assertRaises(mtgdb.exceptions.InvalidDataError,
                                  self.content.available_sets,
                                  True)
                self.assertTrue(get.called)
                args = get.call_args
                self.assertEqual(args[0][0], self._url,
                                 "Wrong URL called in requests.get():" + args[0][0])

    def test_shouldReturnExceptionIfTheZipCannotBeReadFromInternet(self):
        with tests.test_utils.FileMocker() as f_mocker:
            # file does not exist locally
            f_mocker.register_file(self._path, False, "")

            with mock.patch('mtgdb.core.content_provider.requests.get') as get:
                get.return_value.content = mtgjson_data.faulty_zipped()
                self.assertRaises(mtgdb.exceptions.InvalidDataError,
                                  self.content.available_sets,
                                  True)

    def test_shouldReturnExceptionIfCantAccessInternet(self):
        with tests.test_utils.FileMocker() as f_mocker:
            # file does not exist locally
            f_mocker.register_file(self._path, False, "")

            with mock.patch('mtgdb.core.content_provider.requests.get') as get:
                get.side_effect = requests.exceptions.ConnectionError
                self.assertRaises(mtgdb.exceptions.DataUnavailable,
                                  self.content.available_sets,
                                  True)

    def test_populateShouldAddAvailableInformationToSets(self):
        with tests.test_utils.FileMocker() as f_mocker:
            # file does not exist locally
            f_mocker.register_file(self._path, True, mtgjson_data.data)

            # CASE 1
            data_ids = [
                d_ids.SET_DATA.RELEASE_DATE
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.RELEASE_DATE]),
                                 "case 1: populating set list with release dates not successful")

            # CASE 2
            data_ids = [
                d_ids.SET_DATA.BORDER
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                 [d_ids.SET_DATA.BORDER]),
                                 "case 2: populating set list with borders not successful")

            # CASE 3
            data_ids = [
                d_ids.SET_DATA.BLOCK
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.BLOCK]),
                                 "case 3: populating set list with block not successful")

            # CASE 4
            data_ids = [
                d_ids.SET_DATA.TYPE
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.TYPE]),
                                 "case 4: populating set list with set type not successful")

            # CASE 5
            data_ids = [
                d_ids.SET_DATA.BOOSTER
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.BOOSTER]),
                                 "case 5: populating set list with boosters not successful")

            # CASE 6
            data_ids = [
                d_ids.SET_DATA.OLD_CODE
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.OLD_CODE]),
                                 "case 6: populating set list with old_code not successful")

            # CASE 7
            data_ids = [
                d_ids.SET_DATA.MCI_CODE
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.MCI_CODE]),
                                 "case 7: populating set list with mci_code not successful")

            # CASE 8
            data_ids = [
                d_ids.SET_DATA.GATHERER_CODE
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.GATHERER_CODE]),
                                 "case 8: populating set list with gatherer_code not successful")

            # CASE 9
            data_ids = [
                d_ids.SET_DATA.ONLINE_ONLY
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              [d_ids.SET_DATA.ONLINE_ONLY]),
                                 "case 9: populating set list with online_only not successful")

            # CASE 10
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
        with tests.test_utils.FileMocker() as f_mocker:
            # file does not exist locally
            f_mocker.register_file(self._path, True, mtgjson_data.data)

            # CASE 1
            data_ids = [
                'does_not_exist',
            ]
            sets = self.content.available_sets()
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(data=mtgjson_data.data_extended),
                                 "case 1: does not correctly handle non-available labels")

            # CASE 2
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
        with tests.test_utils.FileMocker() as f_mocker:
            # file does not exist locally
            f_mocker.register_file(self._path, True, mtgjson_data.data)

            # CASE 1
            data_ids = [
                d_ids.SET_DATA.RELEASE_DATE,
            ]
            sets = mtgjson_data.data_sets(mtgjson_data.data_extended, data_ids) #already contains 'release date'
            self.content.populate(sets, data_ids)
            self.assertListEqual(sets, mtgjson_data.data_sets(mtgjson_data.data_extended,
                                                              d_ids.SET_DATA.RELEASE_DATE),
                                 "case 1: wrong population behavior when is data already present")

            # CASE 2
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
        with tests.test_utils.FileMocker() as f_mocker:
            # file does not exist locally
            f_mocker.register_file(self._path, True, mtgjson_data.data)

            # CASE 1
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