import unittest
import mtgdb.content_provider


class LocalProviderTest(unittest.TestCase):

    def setUp(self):
        self.localProvider = mtgdb.content_provider.LocalContentProvider()

    def test_availableSets(self):
        sets = self.localProvider.available_sets()
        self.assertIsNotNone(sets)



if __name__ ==  "__main__":
    unittest.main()