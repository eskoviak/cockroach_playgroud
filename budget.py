import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from models import Expense, Expense_category, Expense_sub_category


class Budget:
    """Budget class represents the budge operations with the datastore

    """

    def __init__(self):
        self._get_allowed_sub_category_stmt = text("""
            SELECT expense_sub_category, esc.id 
            FROM Expense_sub_category AS esc
            JOIN Expense_xref ON expense_sub_category_id = esc.id
            JOIN Expense_category AS ec ON ec.id = expense_category_id
            WHERE ec.expense_category = :category;
            """)

    def _get_session(self) -> sessionmaker:
        """Gets a sessionmaker object
        
        Opens the cockroach instance based on the URL and returns the sessionmaker object which can be used by other routines.
        """
        psycopg_uri = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        return sessionmaker(bind=create_engine(psycopg_uri))

    def _insert_expense(self, s: session, details : dict):
        """Internal function to insert into the expense table
        
        """
        new_expense = []
        for detail in details:          # holds the Expense objects to be inserted
            expense_category = s.query(Expense_category).filter(Expense_category.expense_category == detail['expense_category']).first()
            expense_sub_category = s.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == detail['expense_sub_category']).first()

            new_expense.append(Expense(
                date = detail['date'],
                expense_category_id = expense_category.id,
                expense_sub_category_id = expense_sub_category.id,
                amount = detail['amount'],
                tender = detail['tender'],
                expense_detail = json.dumps(detail['expense_detail'])
            ))
        s.add_all(new_expense)    

    def bulk_load(self, filename : str) -> dict():
        """loads the filename and returns a dict object with entries for each receipt

        Args:
            filename (str): [JSON file with receipt data]

        Raises:
            FileNotFoundError: [returned if the input file cannot be found.]

        Returns:
            [dict]: [a dictionary object with the expense line items.]
        """
        assert filename.__len__() > 0, 'filename not specified'
        try:
            fp = open(filename, mode='r', encoding='utf-8')
            return json.load(fp)["receipts"]
        except FileNotFoundError as fne:
            print(f"File not found: ${fne.filename}")
            raise  FileNotFoundError

    def add_expense(self, details: dict() ):
        """public wrapper for the interal insert function

        Args:
            details (dict): [the dictionary containing the expense line items]
        """

        run_transaction(self._get_session(), 
            lambda s : self._insert_expense(s, details))

    def get_expense_categories() -> dict():
        """returns a dict object of expense categories
        
        Format:   { expense_category.name : expense_category.id}
        """
        items = run_transaction(self._get_session(), 
            lambda s : s.query(Expense_category))

        expense_categories = {}
        for item in items:
            expense_categories[item.expense_category] = item.id

        return expense_categories

    def get_sub_categories(self, c : str) -> dict():
        """Returns the list of expense_sub_categories for a given category
        
        """
        result =  run_transaction(self._get_session(), 
            lambda s : s.execute(self._get_allowed_sub_category_stmt.bindparams(category=c)))

        expense_sub_categories = {}
        for t in result.all():
            expense_sub_categories[t[0]] = t[1]
        
        return expense_sub_categories