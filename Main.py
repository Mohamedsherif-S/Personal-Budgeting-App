import sys
import Storage
from Admin         import Admin
from User          import User
from Budget        import Budget
from Category      import Category
from Goal          import Goal, GoalManager
from Notification import Notification
from Report        import Report
from Transection  import Transaction
from Menu          import Menu

def main():
    """
    Main entry point of the application. 
    Initializes all core modules and starts the menu.
    """
    # Initialize notification and goal management first
    notification = Notification()
    goal         = Goal()
    goal_manager = GoalManager(goal, notification)

    # Initialize other system components
    admin       = Admin()
    user        = User("", "", "", "", "") # Placeholder user instance
    transaction = Transaction()
    budget      = Budget()
    category    = Category()
    report      = Report()

    # Pass all instances to the Menu handler to start the UI
    menu = Menu(
        user=user,
        admin=admin,
        goal_manager=goal_manager,
        transaction=transaction,
        budget=budget,
        report=report,
        category=category,
    )
    
    # Run the welcome screen
    menu.show_welcome()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle manual exit (Ctrl+C) gracefully
        print("\n\n  Goodbye!\n")
        sys.exit(0)
