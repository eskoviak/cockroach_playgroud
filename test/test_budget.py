import unittest
from unittest.mock import (
    MagicMock
)

from budget import Budget

class TestAuxFunctions(unittest.TestCase):

    def setUp(self):
        self.budget = Budget()

    #def test_bulk_load_csv_empty_file(self):
    #    with self.assertRaises(AssertionError):
    #        self.budget.bulk_load_csv('')

    def test_bulk_load_csv_fnf(self):
        with self.assertRaises(FileNotFoundError):
            self.budget.bulk_load_csv('bogus.file')

    def test_bulk_load_csv_valid(self):
        data = self.budget.bulk_load_csv('data/test/test-Budget Input_valid.csv')
        self.assertEquals(None, self.budget.validate_input(data))

    #def test_get_expense_categories(self):
    #    self.budget.get_expense_categories = MagicMock(return_value = {"Vehicle": 123456789})
    #    self.assertCountEqual(self.budget.get_expense_categories(), {"Vehicle": 123456789})


if __name__ == '__main__':
    unittest.main()
