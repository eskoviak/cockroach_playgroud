"""models_pg.py -- contains the ORM models used in the application for Postgresql14

"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values

metadata_obj = MetaData(schema='finance')
Base = declarative_base(metadata=metadata_obj)

#redefining from cockroach to local postgresql
class Expense_category(Base):
    """  The accounting category to which the expense is assigned

    """
    __tablename__ = 'expense_category'

    id = Column(BigInteger, primary_key=True)                   #: the id column
    expense_category = Column(String(20), nullable=False)       #: the expense category

    def __repr__(self):
        return(f"Expense_Category (Id: {self.id}, Expense_category: {self.expense_category}")

class Expense_sub_category(Base):
    """ The sub-category of the expense

    """
    __tablename__ = 'expense_sub_category'

    id = Column(BigInteger, primary_key=True)                  #: the id column
    expense_sub_category = Column(String(20), nullable=False)  #: the expnese sub-category

    def __repr__(self):
        return (f"Expense_sub_category: (id {self.id}, expense_sub_category: {self.expense_sub_category})")

class Expense_xref(Base):
    """ The Expense_xref class contains the allowable combinations of expense_sub_categories and expense_categories
    
    """
    __tablename__ = 'expense_xref'

    id = Column(Integer, primary_key=True, autoincrement=True)                                                               #: the id column
    expense_category_id = Column(BigInteger, ForeignKey('expense_category.id'), nullable=False)             #: fk to expense category
    expense_sub_category_id = Column(BigInteger, ForeignKey('expense_sub_category.id'), nullable=False)     #: fk to expense sub-category

    def __repr__(self):
        return (f"Expense_xref: (id {self.id}, expense_category_id {self.expense_category_id}, expense_sub_category_id {self.expense_sub_category_id}")


class Expense(Base):
    """  The expense class documents all expenses

    """
    __tablename__ = 'expense'

    id = Column(Integer, autoincrement=True, primary_key=True)                                  #: the id column
    date = Column(DateTime, nullable=False)                                                     #: the date of the expense (UTC)
    expense_category_id = Column(BigInteger, ForeignKey('expense_category.id'), nullable=False) #: the id of the expense category
    expense_sub_category_id = Column(BigInteger, ForeignKey('expense_sub_category.id'), nullable=False)
                                                                                                #: the id of the expense sub-category
    amount = Column(Float(asdecimal=True), nullable=False)                                      #: amount of the expense
    tender = Column(String(50))                                                                 #: the form of tender
    expense_detail = Column(Text)                                                               #: expense particular details
    memo = Column(Text)                                                                         #: memo

    
#####
# Executtion Wrapper -- if this class is executed, any/all classes will be 
# instantiated
#####
if __name__ == '__main__':

    config = dotenv_values(".env")

    try:
        engine = create_engine(config['POSTGRES_URI']+'finance')
        Base.metadata.create_all(engine)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

