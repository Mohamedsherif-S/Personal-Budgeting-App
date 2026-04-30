
 
import sys
import Storage
 
# ── Import all existing team classes ──────────────────────────────────────────
from Admin             import Admin
from User              import User
from Budget            import Budget
from Category          import Category
from Dashboard         import Dashboard
from ExternalBankSystem import ExternalBankSystem
from Goal              import Goal
from Notification      import Notification
from Report            import Report
from Transection       import Transaction   # note: team file is "Transection.py"
 
# ── Import new orchestrators (your assigned work) ─────────────────────────────
from BankSync          import BankSync
from Goal       import GoalManager
from Menu              import Menu
 
 
def bootstrap_user():
    
    users = Storage.load_users()
 
    if users:
        # Use the first stored user as the "current" user object
        uid, data = next(iter(users.items()))
        user = User(
            user_id  = data["user_id"],
            username = data["username"],
            email    = data["email"],
            password = data["password"],
            phone    = data.get("phone", ""),
        )
        user.balance = data.get("balance", 0.0)
        return user
 
    # No users yet — placeholder (overwritten on register)
    return User(
        user_id  = "U001",
        username = "",
        email    = "",
        password = "",
        phone    = ""
    )
 
 
def main():
    print("\n  Loading data...")
 
    # ── Instantiate all classes ───────────────────────────────────────────────
    user             = bootstrap_user()
    admin            = Admin()
    budget           = Budget()
    category         = Category()
    dashboard        = Dashboard()
    external_bank    = ExternalBankSystem()
    goal             = Goal()
    notification     = Notification()
    report           = Report()
    transaction      = Transaction()
 
    # ── Wire orchestrators with their dependencies ────────────────────────────
    bank_sync    = BankSync(user, external_bank, transaction, category, budget, notification)
    goal_manager = GoalManager(goal, notification)
 
    # ── Build and launch the menu ─────────────────────────────────────────────
    menu = Menu(
        user         = user,
        bank_sync    = bank_sync,
        goal_manager = goal_manager,
        transaction  = transaction,
        budget       = budget,
        report       = report,
        dashboard    = dashboard,
        category     = category
    )
 
    menu.show_welcome()
 
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted — goodbye!\n")
        sys.exit(0)
 