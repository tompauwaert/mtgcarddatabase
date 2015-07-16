import unittest
import mock

import mtgdb.core.data_view
import tests.data.mtgjson_testdata as mtgjson_data
from mtgdb.core.data_id import SET_DATA as s_id

class DataViewTest(unittest.TestCase):

    def setUp(self):
        self.data_view = mtgdb.core.data_view.DataView()

    @mock.patch('mtgdb.core.data_view.content_provider.ContentAvailability.available_sets')
    def test_shouldListAvailableSetsWithRequestedInformation_Available(self, m_av):
        m_av.return_value = mock.MagicMock()
        sets = self.data_view.available_sets([s_id.RELEASE_DATE])
        self.assertListEqual(sets,
                             mtgjson_data.data_sets([s_id.RELEASE_DATE]),
                             "release dates not correct in set information")





def suite():
    test_cases = [
        DataViewTest,
    ]
    suite = unittest.TestSuite()
    for test in test_cases:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test))
    return suite
