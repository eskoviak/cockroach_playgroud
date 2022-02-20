--expense_category = 'Liability';
--expense_sub_category_id int;

SET expense_category_id = (SELECT id FROM expense_category WHERE expense_category = 'Liability');
