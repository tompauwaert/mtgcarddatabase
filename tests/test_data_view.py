import unittest
import mock

import mtgdb.core.data_view
import tests.data.mtgjson_testdata as mtgjson_data
from mtgdb.core.data_labels import SET_LABELS

class DataViewTest(unittest.TestCase):

    def setUp(self):
        self.data_view = mtgdb.core.data_view.DataView()

    @mock.patch('mtgdb.core.data_view.content_provider.ContentAvailability.available_sets')
    def test_shouldListAvailableSetsWithRequestedInformation_Available(self, m_av):
        pass




def suite():
    test_cases = [
        DataViewTest,
    ]
    suite = unittest.TestSuite()
    for test in test_cases:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test))
    return suite
