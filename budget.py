"""Module Budget

Data Access Object to budget database
"""
import json
import csv
import os
import datetime
from copy import deepcopy
import pandas as pd
#from unicodedata import category
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import session, sessionmaker, Session
from sqlalchemy_cockroachdb import run_transaction
import boto3
from dotenv import dotenv_values
from smart_open import open
from models import Expense, Expense_category, Expense_sub_category, Expense_xref
class Budget:
    """Budget class represents the budget operations with the datastore

    """

    #_cert_location : str = ''

    def __init__(self):
        self._get_allowed_sub_category_stmt = text("""
            SELECT expense_sub_category, esc.id 
            FROM Expense_sub_category AS esc
            JOIN Expense_xref ON expense_sub_category_id = esc.id
            JOIN Expense_category AS ec ON ec.id = expense_category_id
            WHERE ec.expense_category = :category;
            """)
        self.config = dotenv_values('.env')
        self._psycopg_uri = f"cockroachdb://{self.config['COCKROACH_ID']}@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert={self.config['HOME']}/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123"

    def _check_data(self, s : session, data : list) -> list:
        """checks the expense categoroy/expense sub categories in the input

        :param data: the input list to be checked
        :type data: dict
        :return: a list of errors, empty is none
        :rtype: list

        Validation rules:
        Each expense_categoy must exist in the Expense_Category object AND
        Each expense_sub_category must exist in the Expense_Sub_Category object AND
        The expense_sub_category must be *allowed* in the Expense_xref object
        """

        data_errors = []
        for record in data:
            try:
                test = pd.to_datetime(record['date'], utc=True)
            except BaseException as err:
                data_errors.append(f"{err}")
                continue
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

        :return: a session
        :rtype: sessionmaker
        
        Opens the cockroach instance based on the URL and returns the sessionmaker object which can be used by other routines.
        """
        #psycopg_uri = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/home/eskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        #psycopg_uri = f"cockroachdb://{os.environ['COCKROACH_ID']}@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert={os.environ['HOME']}/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123"
        return sessionmaker(bind=create_engine(self._psycopg_uri))

    def _insert_expense(self, s: session, details : dict):
        """Internal function to insert into the expense table
        
        """
        new_expense = []
        for detail in details:          # holds the Expense objects to be inserted
            expense_category = s.query(Expense_category).filter(Expense_category.expense_category == detail['expense_category'].strip()).first()
            expense_sub_category = s.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == detail['expense_sub_category'].strip()).first()

            new_expense.append(Expense(
                #date = pd.to_datetime(detail['date'], utc=True),
                date = detail['date'],
                expense_category_id = expense_category.id,
                expense_sub_category_id = expense_sub_category.id,
                amount = detail['amount'],
                tender = detail['tender'],
                expense_detail = detail['expense_detail'],
                memo = detail['memo'])
            )
        return(s.add_all(new_expense))

    def _archive_s3(self, filename : str) -> bool:
        """creates a copy of filename in ../Archive with timestamp

        :param filename: The filename to archive
        :type filename: str
        :return: True if achive successful, False if not
        :rtype: bool
        """
        bucket_name = self.config['S3_BUCKET']
        key = f"Data Sets/{filename}"
        fn_parts = os.path.basename(key).split('.')
        date_stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        archive_key = f"Data Sets/Archive/{fn_parts[0]}_{date_stamp}.{fn_parts[1]}"
        _s3_client = boto3.client('s3', aws_access_key_id=self.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.config['AWS_SECRET_ACCESS_KEY'])

        response = _s3_client.copy_object(
            Bucket = bucket_name,
            CopySource = f"{bucket_name}/{key}",
            Key = archive_key,
        )
        return(True if response['ResponseMetadata']['HTTPStatusCode']==200 else False)

    def _add_expense_category(self, s : session, expense_cat : str) :
        """Add expense category.

        Caller should have checked to see if it existed

        """
        new_category = Expense_category(expense_category = str(expense_cat))
        return(s.add(new_category))

    def _add_expense_sub_category(self, s : session, expense_sub_cat : str) -> int:
        """Add a sub-category to the expense_sub_category table, if it doesn't exist.
        
        :param expense_sub_cat: The sub-category to add
        :type expense_sub_cat: str
        :return: the id of the new sub-cateogory 
        :rtype: int

        If the expense_sub_cat exists, return the id.  Otherwise add the expense sub-category.  Since adding to xref uses ids, it
        isn't necessary to duplicate the sub
        """
        result = select(Expense_sub_category).where(Expense_sub_category.expense_sub_category.in_([expense_sub_cat]))
        for sub_cat in s.scalars(result):
            print(sub_cat)
        
    def bulk_load_s3(self, filename : str) -> list:
        """loads the csv file from S3 using environmental variables

        :param filename: The filename of the remote file.  Note that pathing off of the bucket must be included
        :type filename: str
        :return: a list of dict objects representing the csv fields
        :rtype: list

        """
        urn = f"{self.config['S3_BUCKET']}/{filename}"
        s3_uri = f"s3://{self.config['AWS_ACCESS_KEY_ID']}:{self.config['AWS_SECRET_ACCESS_KEY']}@{urn}"

        with open(s3_uri) as s3file:
            reader = csv.DictReader(s3file)
            expenses = []
            for row in reader:
                ## The detail is stored as a stringified JSON object
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
                """The detail is stored as a stringified JSON object
                """
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

        Validation rules:
        Each expense_categoy must exist in the Expense_Category object AND
        Each expense_sub_category must exist in the Expense_Sub_Category object AND
        The expense_sub_category must be *allowed* in the Expense_xref object
        """
        return(run_transaction(self._get_session(),
            lambda s : self._check_data(s, details)))

    def add_expense(self, details: dict() ):
        """public wrapper for the interal insert function

        :param details: Dictionary containing the expenses to be added
        :type details: dict
        :return: 
        """

        if len(test := self.validate_input(details)) != 0:
            print(f"data is invalid {test}")
        else:
            run_transaction(self._get_session(), 
                lambda s : self._insert_expense(s, details))

    def add_expense_category(self, expense_category : str) -> int:
        """Add expense category

        :param expense_category: The category text to add
        :type expense_category: str
        :return: status -1 if the category exists, 1 if added, 0 if other error occurred
        :rtype: int

        Check to see if the expense category exists; if it does, return an error (-1), if not add it, check to see if it has been added.


        """
        if expense_category in self.get_expense_categories():
            return -1
        else:
            run_transaction(self._get_session(),
              lambda s: self._add_expense_category(s, expense_category))
            if expense_category in self.get_expense_categories():
                return 1
            else:
                return 0

    def add_expense_sub_category(self, expense_sub_cat : str) -> int:
        """return the id of the existing or newly created expense sub-category
        
        :param expense_sub_cat: The value to fetch or add
        :type expense_sub_cat: str
        :return: the id of the item (new or existing)
        :rtype: int
        
        """
        return self._add_expense_sub_category(self._get_session(), expense_sub_cat)

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

    def get_sub_categories(self, category : str) -> dict():
        """Returns the list of expense_sub_categories for a given category

        :param category: expense category
        :type category: str
        :return: dictionary of expense
        :rtype: dict
        
        """
        result =  run_transaction(self._get_session(), 
            lambda s : s.execute(self._get_allowed_sub_category_stmt.bindparams(category=category)))

        expense_sub_categories = {}
        for row in result.all():
            expense_sub_categories[row[0]]=row[1]
        
        return expense_sub_categories

    def get_chart_of_accounts(self) -> dict:
        """gets the Chart Of Accounts

        :return: the chart of accounts
        :rtype: dict

        The return dictionary has the following structure:

        { <category> : [sub_category, ...]}

        """
        coa = {}
        sub_categories = []
        for category in self.get_expense_categories().keys():
            #print(category)
            sub_categories.clear()
            for sub_category in self.get_sub_categories(category).keys():
                sub_categories.append(sub_category)
            coa[category] = deepcopy(sub_categories)

        return coa

    def backup_database(self):
        """performs a full backup of the database to s3
        
        """
        stmt = f"BACKUP DATABASE budget TO 's3://{self.config['S3_BUCKET']}/Cockroach Data/budget_backups?aws_access_key_id={self.config['AWS_ACCESS_KEY_ID']}&aws_secret_access_key={self.config['AWS_SECRET_ACCESS_KEY']}' AS OF SYSTEM TIME '-10s';"
        engine = create_engine(self._psycopg_uri)
        result = engine.execute(stmt)


        print(result)
        
