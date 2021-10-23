import re
from sqlalchemy import create_engine
from sqlalchemy.sql.elements import True_
from sqlalchemy.sql.expression import null, nullslast
from sqlalchemy.sql.operators import as_
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, Table
#from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    """  The expense class documents all expenses
    """

    __tablename__ = 'expense'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, nullable=False)
    expense_category_id = Column(Integer, ForeignKey('expense_category.id'), nullable=False)
    expense_sub_category_id = Column(Integer, ForeignKey('expense_sub_category.id'), nullable=False)
    amount = Column(Float(asdecimal=True), nullable=False)
    tender = Column(String(50))
    expense_detail = Column(Text)

class Expense_sub_category(Base):
    ''' The sub-category of the expense
    '''

    __tablename__ = 'expense_sub_category'

    id = Column(Integer, autoincrement=True, primary_key=True)
    expense_sub_category = Column(String(25), nullable=False)

    def __repr__(self):
        return (f"Expense_sub_category: (id {self.id}, expense_sub_category: {self.expense_sub_category})")

class Expense_xref(Base):
    #The xref which ties allowable sub-categories to to categories

    __tablename__ = 'expense_xref'

    id = Column(Integer, autoincrement=True, primary_key=True)
    expense_category_id = Column(Integer, ForeignKey('expense_category.id'), nullable=False)
    expense_sub_category_id = Column(Integer, ForeignKey('expense_sub_category.id'), nullable=False)
    #expense_sub_category = relationship("Expense_sub_category")
    #expense_category = relationship("Expense_category")

class Expense_category(Base):
    '''  The accounting category to which the expense is assigned
    '''
    __tablename__ = 'expense_category'

    id = Column(Integer, autoincrement=True, primary_key=True)
    expense_category = Column(String(25), nullable=False)
    #expense_sub_categories = relationship("Expense_sub_category", secondary="expense_xref", overlaps="expense_sub_category")

    def __repr__(self):
        return(f"Expense_Category (Id: {self.id}, Expense_category: {self.expense_category}, Childred: {self.expense_sub_categories}")



if __name__ == '__main__':
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    Base.metadata.create_all(engine)
