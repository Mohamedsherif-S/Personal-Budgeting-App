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
    goal_manager = GoalManager(goal, notification)

    menu = Menu(
        user=user, goal_manager=goal_manager,
        transaction=transaction, budget=budget, report=report,
        dashboard=dashboard, category=category,
        bank_sync=external_bank
    )
    menu.show_welcome()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Goodbye!\n")
        sys.exit(0)
