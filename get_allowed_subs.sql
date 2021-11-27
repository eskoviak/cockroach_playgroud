--SELECT expense_sub_category, id 
--FROM Expense_sub_category
--WHERE  id IN 
--    (SELECT expense_sub_category_id FROM Expense_xref
--    WHERE expense_category_id = (
--        SELECT id FROM Expense_category WHERE expense_category = 'Misc'
--    )
--);

SELECT expense_sub_category, esc.id 
FROM Expense_sub_category AS esc
JOIN Expense_xref ON expense_sub_category_id = esc.id
JOIN Expense_category AS ec ON ec.id = expense_category_id
WHERE ec.expense_category = 'Personal';
