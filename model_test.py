import datetime
import json

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.sqltypes import Date, TEXT
from sqlalchemy_cockroachdb import run_transaction
import models

def get_sub_categories(session, category):
    #print(session.query(models.Expense_category, models.Expense_category.expense_sub_categories))
    return session.query(models.Expense_category, models.Expense_category.expense_sub_categories)

if __name__ == '__main__':
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    with Session(engine) as s:
        result = s.execute(select(models.Expense_category, models.Expense_category.expense_sub_categories).filter(models.Expense_category.expense_category == 'Misc'))
        print(result.scalars().all())

