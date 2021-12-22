#from ast import Pass
#from collections import namedtuple
import json
import csv
import os
from smart_open import open

#from unicodedata import category
from sqlalchemy import create_engine, text
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from models import Expense, Expense_category, Expense_sub_category, Expense_xref


class Budget:
    """Budget class represents the budge operations with the datastore

    """

    #_data_check = namedtuple('_data_check', [ 'Field', 'Error'])
    _cert_location : str = ''

    def __init__(self):
        self._get_allowed_sub_category_stmt = text("""
            SELECT expense_sub_category, esc.id 
            FROM Expense_sub_category AS esc
            JOIN Expense_xref ON expense_sub_category_id = esc.id
            JOIN Expense_category AS ec ON ec.id = expense_category_id
            WHERE ec.expense_category = :category;
            """)

    def _check_data(self, s : session, data : list) -> list:
        """checks the expense categoroy/expense sub categories in the input

        Each expense_categoy must exist in the Expense_Category object AND
        Each expense_sub_category must exist in the Expense_Sub_Category object AND
        The expense_sub_category must be *allowed* in the Expense_xref object

        Args:
            s ( sesssion ): a session
            input (list): An interable of dictionarey objects

        Returns:
            a list of all the errors found
        """

        data_errors = []
        for record in data:
            result_category = s.query(Expense_category).filter(Expense_category.expense_category == record['expense_category'].strip()).first()
            if result_category == None:
                data_errors.append(f"expense_category {record['expense_category']} not found")
                continue
            else: 
                result_sub_cat = s.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == record['expense_sub_category'].strip()).first()
                if result_sub_cat == None:
                    data_errors.append(f"expense_sub_category {record['expense_sub_category']} not found")
                    continue
                else:
                    result_xref = s.query(Expense_xref).filter(
                            Expense_xref.expense_category_id == result_category.id).filter(
                            Expense_xref.expense_sub_category_id == result_sub_cat.id).first()
                    if result_xref == None:
                        data_errors.append(f"{record['expense_sub_category']} is not an allowed sub-category of {record['expense_category']}")
                        continue
        return data_errors


    def _get_session(self) -> sessionmaker:
        """Gets a sessionmaker object
        
        Opens the cockroach instance based on the URL and returns the sessionmaker object which can be used by other routines.
        """
        #psycopg_uri = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/home/eskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        psycopg_uri = f"cockroachdb://{os.environ['COCKROACH_ID']}@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert={os.environ['HOME']}/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123"
        return sessionmaker(bind=create_engine(psycopg_uri))

    def _insert_expense(self, s: session, details : dict):
        """Internal function to insert into the expense table
        
        """
        new_expense = []
        for detail in details:          # holds the Expense objects to be inserted
            expense_category = s.query(Expense_category).filter(Expense_category.expense_category == detail['expense_category'].strip()).first()
            expense_sub_category = s.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == detail['expense_sub_category'].strip()).first()

            new_expense.append(Expense(
                date = detail['date'],
                expense_category_id = expense_category.id,
                expense_sub_category_id = expense_sub_category.id,
                amount = detail['amount'],
                tender = detail['tender'],
                expense_detail = detail['expense_detail'],
                memo = detail['memo'])
            )
        s.add_all(new_expense)    

    def bulk_load_s3(self, filename : str) -> list:
        """loads the csv file from S3 using environmental variables

        :param filename: The filename of the remote file.  Note that pathing off of the bucket must be included
        :type filename: str
        :return: a list of dict objects representing the csv fields
        :rtype: list

        """
        urn = f"{os.environ['DATA_SET_BUCKET']}/{filename}"
        s3_uri = f"s3://{os.environ['AWS_ACCESS_KEY_ID']}:{os.environ['AWS_SECRET_ACCESS_KEY']}@{urn}"

        with open(s3_uri) as s3file:
            reader = csv.DictReader(s3file)
            expenses = []
            for row in reader:
                """"The detail is stored as a stringified JSON object"""
                detail = dict()
                detail["location"] = row["Location"]
                detail["vendor"] = row['Vendor']
                detail['mileage'] = row['Mileage']
                detail['gallons'] = row['Gallons']
                detail['vehicle'] = row['Vehicle']
                detail['balance on account'] = row['Balance_on_account']

                expense = dict()
                expense['expense_category'] = row['Category'].strip()
                expense['expense_sub_category'] = row['SubCategory'].strip()
                expense['expense_detail'] = json.dumps(detail)
                expense['date'] = row['Date']
                expense['amount'] = row['Amount']
                expense['tender'] = row['Tender'].upper()
                expense['memo'] = row['Memo']

                expenses.append(expense)
        return expenses

    

    def bulk_load_csv(self, filename : str):
        """Loads a csv file from the local file system for expense input

        :param filename: The filename of the local file
        :type filename: str
        :return: a list of dict objects representing the csv fields
        :rtype: list

        """
        with open(filename, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            expenses = []
            for row in reader:
                """"The detail is stored as a stringified JSON object"""
                detail = dict()
                detail["location"] = row["Location"]
                detail["vendor"] = row['Vendor']
                detail['mileage'] = row['Mileage']
                detail['gallons'] = row['Gallons']
                detail['vehicle'] = row['Vehicle']
                detail['balance on account'] = row['Balance_on_account']

                expense = dict()
                expense['expense_category'] = row['Category'].strip()
                expense['expense_sub_category'] = row['SubCategory'].strip()
                expense['expense_detail'] = json.dumps(detail)
                expense['date'] = row['Date']
                expense['amount'] = row['Amount']
                expense['tender'] = row['Tender'].upper()
                expense['memo'] = row['Memo']

                expenses.append(expense)
        return expenses


    def bulk_load_json(self, filename : str) -> dict():
        """loads a JSON File from the local file sytemm for expense input

        :param filename: The filename of the remote file.  Note that pathing off of the bucket must be included
        :type filename: str
        :return: a list of dict objects representing the csv fields
        :rtype: list
        """
        assert filename.__len__() > 0, 'filename not specified'
        try:
            fp = open(filename, mode='r', encoding='utf-8')
            return json.load(fp)["receipts"]
        except FileNotFoundError as fne:
            print(f"File not found: ${fne.filename}")
            raise  FileNotFoundError

    def validate_input(self, details: dict() ):
        """validates the data in the input--ensures the expense category and the sub categories exist and are allowwed

        :param details: the input dictionary
        :type details: dict
        :return: list of errors (empty if none found)
        :rtype: list

        """

        return(run_transaction(self._get_session(),
            lambda s : self._check_data(s, details)))

        

    def add_expense(self, details: dict() ):
        """public wrapper for the interal insert function

        Args:
            details (dict): [the dictionary containing the expense line items]
        """

        if len(self.validate_input(details)) != 0:
            print("data is invalid")
        else:
            run_transaction(self._get_session(), 
                lambda s : self._insert_expense(s, details))

    def get_expense_categories(self) -> dict():
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
            expense_sub_categories[t[0]]=t[1]
        
        return expense_sub_categories

    def get_chart_of_accounts(self) -> dict():
        coa = {}
        sub_categories = []
        for category in self.get_expense_categories().keys():
            sub_categories in self.get_sub_categories(category)
            coa[category] = { "sub-categories" : sub_categories.__str__}

        return coa
