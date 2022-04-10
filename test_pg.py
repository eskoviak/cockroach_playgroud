import imp
from sqlalchemy import create_engine, text, select, MetaData
from sqlalchemy.orm import Session
from dotenv import dotenv_values
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base

metadata_obj = MetaData(schema='finance')
Base = declarative_base(metadata=metadata_obj)

config = dotenv_values(".env")

engine = create_engine(config['POSTGRES_URI']+'finance')

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

    id = Column(BigInteger, primary_key=True)                  #: the id column
    expense_category_id = Column(BigInteger, ForeignKey('expense_category.id'), nullable=False)    #: fk to expense category
    expense_sub_category_id = Column(BigInteger, ForeignKey('expense_sub_category.id'), nullable=False)    #: fk to expense sub-category

    def __repr__(self):
        return (f"Expense_xref: (id {self.id}, expense_category_id {self.expense_category_id}, expense_sub_category_id {self.expense_sub_category_id}")

with Session(engine) as session:
    stmt = select(Expense_category)
    result = session.execute(stmt)
    for row in result:
        print(row)
    




