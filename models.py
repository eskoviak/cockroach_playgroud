"""models.py -- contains the ORM models used in the application

"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    """  The expense class documents all expenses

    """
    __tablename__ = 'expense'

    id = Column(Integer, autoincrement=True, primary_key=True)                  #: the id column
    date = Column(DateTime, nullable=False)                                     #: the date of the expense (UTC)
    expense_category_id = Column(Integer, ForeignKey('expense_category.id'), nullable=False) #: the id of the expense category
    expense_sub_category_id = Column(Integer, ForeignKey('expense_sub_category.id'), nullable=False) #: the id of the expense sub-category
    amount = Column(Float(asdecimal=True), nullable=False)                      #: amount of the expense
    tender = Column(String(50))                                                 #: the form of tender
    expense_detail = Column(Text)                                               #: expense particular details
    memo = Column(Text)                                                         #: memo

class Expense_sub_category(Base):
    """ The sub-category of the expense

    """
    __tablename__ = 'expense_sub_category'

    id = Column(Integer, autoincrement=True, primary_key=True)                  #: the id column
    expense_sub_category = Column(String(25), nullable=False)                   #: the expnese sub-category

    def __repr__(self):
        return (f"Expense_sub_category: (id {self.id}, expense_sub_category: {self.expense_sub_category})")

class Expense_xref(Base):
    """ The Expense_xref class contains the allowable combinations of expense_sub_categories and expense_categories
    
    """
    __tablename__ = 'expense_xref'

    id = Column(Integer, autoincrement=True, primary_key=True)                  #: the id column
    expense_category_id = Column(Integer, ForeignKey('expense_category.id'), nullable=False)    #: fk to expense category
    expense_sub_category_id = Column(Integer, ForeignKey('expense_sub_category.id'), nullable=False)    #: fk to expense sub-category

    def __repr__(self):
        return (f"Expense_xref: (id {self.id}, expense_category_id {self.expense_category_id}, expense_sub_category_id {self.expense_sub_category_id}")

class Expense_category(Base):
    """  The accounting category to which the expense is assigned

    """
    __tablename__ = 'expense_category'

    id = Column(Integer, autoincrement=True, primary_key=True)                  #: the id column
    expense_category = Column(String(25), nullable=False)                       #: the expense category

    def __repr__(self):
        return(f"Expense_Category (Id: {self.id}, Expense_category: {self.expense_category}, Childred: {self.expense_sub_categories}")

class Test(Base):
    """ A test table for use in testing
    
    """
    __tablename__ = 'test'

    id = Column(Integer, autoincrement=True, primary_key=True)                  #: the id column
    string = Column(String(25), nullable=False)                                 #: the string column used for testing


#####
# Executtion Wrapper -- if this class is executed, any/all classes will be 
# instantiated
#####
if __name__ == '__main__':
    try:
        psycopg_uri = url = 'cockroachdb://ed:Kh4V3R9B7DcygecH@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&sslrootcert=/Users/edmundlskoviak/.postgresql/ca.crt&options=--cluster%3Dgolden-dingo-2123'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    Base.metadata.create_all(engine)
