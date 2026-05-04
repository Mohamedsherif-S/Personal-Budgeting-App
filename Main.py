import sys
import Storage
from Admin        import Admin
from User         import User
from Budget       import Budget
from Category     import Category
from Goal         import Goal, GoalManager
from Notification import Notification
from Report       import Report
from Transection  import Transaction
from Menu         import Menu


def main():
    notification = Notification()
    goal         = Goal()
    goal_manager = GoalManager(goal, notification)

    admin       = Admin()
    user        = User("", "", "", "", "")
    transaction = Transaction()
    budget      = Budget()
    category    = Category()
    report      = Report()

    menu = Menu(
        user=user,
        admin=admin,
        goal_manager=goal_manager,
        transaction=transaction,
        budget=budget,
        report=report,
        category=category,
    )
    menu.show_welcome()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Goodbye!\n")
        sys.exit(0)
