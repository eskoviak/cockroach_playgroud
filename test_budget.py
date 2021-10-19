import unittest
from unittest.mock import (
    MagicMock
)

from budget import Budget

class TestAuxFunctions(unittest.TestCase):

    def setUp(self):
        self.budget = Budget()

    def test_bulk_load_empty_file(self):
        with self.assertRaises(AssertionError):
            self.budget.bulk_load('')

    def test_bulk_load_fne(self):
        with self.assertRaises(FileNotFoundError):
            self.budget.bulk_load('bogus.file')

    def test_bulk_load_valid(self):
        data = self.budget.bulk_load('json/test-receipt.json')
        self.assertEquals(data[0]['amount'], 2000)

    def test_get_expense_categories(self):
        self.budget.get_expense_categories = MagicMock(return_value = {"Vehicle": 123456789})
        self.assertCountEqual(self.budget.get_expense_categories(), {"Vehicle": 123456789})


if __name__ == '__main__':
    unittest.main()
