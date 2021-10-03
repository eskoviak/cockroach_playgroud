SELECT expense_sub_category, id 
FROM Expense_sub_category
WHERE  id IN 
    (SELECT expense_sub_category_id FROM Expense_xref
    WHERE expense_category_id = (
        SELECT id FROM Expense_category WHERE expense_category = 'Misc'
    )
);