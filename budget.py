import datetime
import json

from sqlalchemy import create_engine, text
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy_cockroachdb import run_transaction

from models import Expense, Expense_category, Expense_sub_category

def get_expense_categories(session):
    expense_categories = {}
    items = session.query(Expense_category)
    for item in items:
        expense_categories[item.expense_category] = item.id

    return expense_categories

def get_expense_sub_categories(session, category):
    expense_sub_categories = {}
    items = session.query(Expense_sub_category, Expense_sub_category.expense_sub_category, Expense_sub_category.id).\
                    join(

        )
        

get_allowed_sub_category_stmt = text("""
SELECT expense_sub_category, esc.id 
FROM Expense_sub_category AS esc
JOIN Expense_xref ON expense_sub_category_id = esc.id
JOIN Expense_category AS ec ON ec.id = expense_category_id
WHERE ec.expense_category = :category;
""")

def get_sub_categories(s, c):
    return s.execute(get_allowed_sub_category_stmt.bindparams(category=c))

def add_expense(session, detail):
    new_expense = []

    #print(detail)
    expense_category = session.query(Expense_category).filter(Expense_category.expense_category == detail['expense_category']).first()
    expense_sub_category = session.query(Expense_sub_category).filter(Expense_sub_category.expense_sub_category == detail['expense_sub_category']).first()

    new_expense.append(Expense(
        date = detail['date'],
        expense_category_id = expense_category.id,
        expense_sub_category_id = expense_sub_category.id,
        amount = detail['amount'],
        tender = detail['tender'],
        expense_detail = json.dumps(detail['expense_detail'])
    ))

    session.add_all(new_expense)

'''
from dataclasses import dataclass, asdict
@dataclass
class Detail:
        expense_category : str
        expense_sub_category : str
        expense_detail : dict
        date : str
        amount: float
        tender : str
'''

import json
def bulk_load(filename) -> list():
    fp = open(filename, 'r')
    return json.load(fp)['receipts']




if __name__ == '__main__':
    '''
    item = Detail(
        expense_category = 'Misc',
        expense_sub_category = 'Grocery',
        #expense_detail = {'location' : 'Red Wing, MN', 'vendor': 'Simple Abundance', 'Balance on Account' : 41.08},
        expense_detail = {'location' : ', Red Wing, MN', 'vendor' : 'Target'},
        #expense_detail = {'location' : 'Red Wing, MN', 'gallons' : 15.186, 'mileage' : 162471},
        #expense_detail = { 'location' : 'Online', 'vendor' : 'Zoom'},
        date = '2021-10-09T20:13:00Z',
        amount = 10.18,
        tender = 'amex applepay *2008'
    )
    '''
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

#    for item in bulk_load('./json/receipt.json'):
#        #print(item)
#        run_transaction(sessionmaker(bind=engine),
#            lambda s : add_expense(s, item))

#    print(run_transaction(sessionmaker(bind=engine),
#        lambda s : get_categories(s)))

    result = run_transaction(sessionmaker(bind=engine),
        lambda s : get_sub_categories(s,'Misc'))

    for row in result:
        print(row)
