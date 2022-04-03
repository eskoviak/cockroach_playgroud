import curses
from distutils.command.build import build
from nis import match
from secrets import choice
from budget import Budget
from curses import curs_set, wrapper

from models import Expense_sub_category

def main(stdscr):
    """Main window routine (uses curses)

    :param stdscr: the stdscr object forwarded by the wrapper
    :type stdscr: curses.windown
    :return: None
    :rtype: None

    Screen Layout:

    0 Title
    1,2 to 8,2 User area
    9,2 to 12,2 Menu actions 
    """
    while True:
        # clear screen
        stdscr.clear()
        stdscr.addstr(0, 0, 'Budget Utilities Main Menu'.upper(),
                        curses.A_REVERSE)
        stdscr.addstr(1, 2, 'Add (e)xpense category')
        stdscr.addstr(2, 2, 'Add expense(s)ub-cateogory')
        stdscr.addstr(10, 2, '(q)uit')
        stdscr.refresh()
        stdscr.addstr(12, 1, 'Enter your choice:  ')
        choice = stdscr.getkey()
        if choice == 'q':
            break
        if choice == 'e':
            add_expense(stdscr)
        if choice == 's':
            add_expense_category(stdscr)


def add_expense(stdscr):
    curses.echo()
    stdscr.addstr(8, 2, 'Expense Category to add: ')
    stdscr.clrtobot()
    expense_category = str(stdscr.getstr(),'utf-8')
    curses.noecho()
    result = Budget().add_expense_category(expense_category)
    if result == -1:
        stdscr.addstr(9, 2, 'Category Exists -- aborting')
    elif result == 1:
        stdscr.addstr(9, 2, f"Category added: {result}")
    else:
        stdscr.addstr(9,2, f"Unknown error occured")
    stdscr.addstr(10, 2, 'Press any key to continue...')
    stdscr.getkey()

def add_expense_category(stdscr):
    curses.echo()
    stdscr.addstr(9,2, 'Expense Category to add sub-category to: ')
    stdscr.clrtobot()
    expense_category = str(stdscr.getstr(), 'utf-8')
    if (expense_category == '') | (expense_category == None) : return
    coa = Budget().get_chart_of_accounts()
    if expense_category not in coa.keys():
        stdscr.addstr(10,2, f"Expense category {expense_category} not found in Chart of Accounts--please add the expense category first")
    else:
        stdscr.addstr(10,2, f"Expense sub-category to add to {expense_category}: ")
        expense_sub_category = str(stdscr.getstr(), 'utf-8')
        if (expense_sub_category == '') | (expense_category == None) : return
        if expense_sub_category in coa[expense_category]:
            stdscr.addstr(11,2, f"Expense sub-cateogory {expense_sub_category} already exists on {expense_category}")
        else:
            stmt = f"""
                INSERT INTO Expense_xref (expense_category_id, expense_sub_category_id)
                VALUES ( (SELECT id FROM Expense_category WHERE expense_category = {expense_category}),
                (SELECT id FROM Expense_sub_category WHERE expense_sub_category = {expense_sub_category}));
            """
            print(stmt)

    curses.noecho()

    stdscr.addstr(12, 2, 'Press any key to continue...')
    stdscr.getkey()

if __name__ == '__main__':
    """Top Level Program

    """
    wrapper(main)
