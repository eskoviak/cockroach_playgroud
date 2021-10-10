import datetime
import json

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy_cockroachdb import run_transaction
from models import Expense_category, Expense_sub_category, Expense_xref


stmt = '''
SELECT expense_sub_category, esc.id 
FROM Expense_sub_category AS esc
JOIN Expense_xref ON expense_sub_category_id = esc.id
JOIN Expense_category AS ec ON ec.id = expense_category_id
WHERE ec.expense_category = 'Misc';
'''
def get_sub_categories(session, category):
    #print(session.query(models.Expense_category, models.Expense_category.expense_sub_categories))
    return session.query(Expense_category, Expense_category.expense_sub_categories)

if __name__ == '__main__':
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    with Session(engine) as s:
        result = s.execute(select(Expense_category, Expense_category.expense_sub_categories).filter(Expense_category.expense_category == 'Misc'))
        #result = s.execute(text(stmt))
        for row in result.scalars():
            print(row)

