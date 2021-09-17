from sqlalchemy.sql.elements import True_
from sqlalchemy.sql.expression import nullslast
from sqlalchemy.sql.operators import as_
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text
#from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import Date

Base = declarative_base()

class Expense(Base):
    """  The expense class documents all expenses
    """

    __table__ = 'expense'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, nullable=False)
    expense_category_id = Column(Integer, ForeignKey('expense_category.id'), nullable=False)
    expense_sub_category_id = Column(Integer, ForeignKey('expense_sub_category.id'), nullable=False)
    amount = Column(Float(asdecimal=True), nullable=False)
    tender = Column(String(50))
    expense_detail = Column(Text)

class Expense_category(Base):
    '''  The accounting category to which the expense is assigned
    '''
    __table__ = 'expense_category'

    id = Column(Integer, autoincrement=True, primary_key=True)
    expense_category = Column(String(25), nullable=False)

class Expense_sub_category(Base):
    ''' The sub-category of the expense
    '''

    __table__ = 'expense_sub_category'

    id = Column(Integer, primary_key=True)
    expense_sub_category = Column(String(25), nullable=False)

class Expense_xref(Base):
    ''' The xref which ties allowable sub-categories to to categories
    '''

    __table__ = 'expense_xref'

    expense_category_id = Column(Integer, ForeignKey('expense_category.id'))
    expense_sub_category_id = Column(Integer, ForeignKey('expense_sub_category.id'))
