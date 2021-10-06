INSERT INTO Expense_category (expense_category) VALUES ('Business');

INSERT INTO Expense_sub_category (expense_sub_category) VALUES ('Services');

INSERT INTO Expense_xref (expense_category_id, expense_sub_category_id)
  VALUES ( (SELECT id FROM Expense_category WHERE expense_category = 'Business'),
  (SELECT id FROM Expense_sub_category WHERE expense_sub_category = 'Services'));