import sys
import Storage
from Admin          import Admin
from User           import User
from Budget         import Budget
from Category       import Category
from Dashboard      import Dashboard
from ExternalBankSystem import ExternalBankSystem
from Goal           import Goal, GoalManager
from Notification   import Notification
from Report         import Report
from Transection    import Transaction
from BankSync       import BankSync
from Menu           import Menu

def main():
    user         = User("", "", "", "", "")
    notification = Notification()
    goal         = Goal()
    transaction  = Transaction()
    budget       = Budget()
    category     = Category()
    report       = Report()
    dashboard    = Dashboard()
    external_bank = ExternalBankSystem()
    bank_sync    = BankSync(user, external_bank, transaction, category, budget, notification)
    goal_manager = GoalManager(goal, notification)

    menu = Menu(
        user=user, bank_sync=bank_sync, goal_manager=goal_manager,
        transaction=transaction, budget=budget, report=report,
        dashboard=dashboard, category=category
    )
    menu.show_welcome()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Goodbye!\n")
        sys.exit(0)