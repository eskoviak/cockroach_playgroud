--INSERT INTO Expense_category (expense_category) VALUES ('Personal');

INSERT INTO Expense_sub_category (expense_sub_category) VALUES ('Houseware');

INSERT INTO Expense_xref (expense_category_id, expense_sub_category_id)
  VALUES ( (SELECT id FROM Expense_category WHERE expense_category = 'Misc'),
  (SELECT id FROM Expense_sub_category WHERE expense_sub_category = 'Houseware'));