import unittest
from budget import bulk_load

class TestAuxFunctions(unittest.TestCase):

    def test_bulk_load_empty_file(self):
        with self.assertRaises(AssertionError):
            bulk_load('')

    def test_bulk_load_fne(self):
        with self.assertRaises(FileNotFoundError):
            bulk_load('bogus.file')



if __name__ == '__main__':
    unittest.main()
