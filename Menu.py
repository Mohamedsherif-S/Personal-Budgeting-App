import datetime
import Storage

class Menu:
    """
    Main controller class for the application UI. 
    Connects users, transactions, budgets, and goals through a CLI menu.
    """
    def __init__(self, user, admin, goal_manager, transaction, budget, report, category):
        """Initializes the menu with all necessary service instances."""
        self.user         = user
        self.admin        = admin
        self.goal_manager = goal_manager
        self.transaction  = transaction
        self.budget       = budget
        self.report       = report
        self.category     = category
        self.session      = None

    
    def show_welcome(self):
        """Displays the initial landing screen for Register or Login."""
        while True:
            print("\n" + "═" * 45)
            print("  💰  Personal Budget Manager")
            print("═" * 45)
            print("  1. Register")
            print("  2. Login")
            print("  0. Exit")
            print("─" * 45)
            choice = input("  → ").strip()
            if   choice == "1": self._register()
            elif choice == "2": self._login()
            elif choice == "0": print("\n  Goodbye! 👋\n"); break
            else: print("  Invalid choice.")

    def _register(self):
        """Handles user registration and creates a new session on success."""
        print("\n── Register ───────────────────────────────────────")
        username = input("  Username : ").strip()
        email    = input("  Email    : ").strip()
        password = input("  Password : ").strip()
        phone    = input("  Phone    : ").strip()
        
        if self.user.register(username, email, password, phone, self.admin):
            print("  ✓ Account created — logging you in...")
            self.session = self.user.generate_session(self.user.user_id)
            self.show_main_menu()

    def _login(self):
        """Authenticates user via email and password."""
        print("\n── Login ──────────────────────────────────────────")
        email    = input("  Email    : ").strip()
        password = input("  Password : ").strip()
        matched  = self.user.find_by_email(email)
        
        if not matched:
            print("  Email not found.")
            return
            
        self.user.load_from_dict(matched)
        if self.user.login(email, password):
            self.session = f"session_{self.user.user_id}"
            self.show_main_menu()
    
    def show_main_menu(self):
        """Core navigation hub once the user is logged in."""
        while True:
            balance = self.user.get_user_balance(self.user.user_id)
            print(f"\n{'═'*45}")
            print(f"  Welcome, {self.user.username}  |  Balance: ${balance:.2f}")
            print("═" * 45)
            print("  1. Add Transaction")
            print("  2. View Transactions")
            print("  3. Manage Budgets")
            print("  4. Goals")
            print("  5. Reports")
            print("  6. Dashboard")
            print("  0. Logout")
            print("─" * 45)
            choice = input("  → ").strip()
            if   choice == "1": self._add_transaction()
            elif choice == "2": self._view_transactions()
            elif choice == "3": self._budget_menu()
            elif choice == "4": self._goals_menu()
            elif choice == "5": self._reports_menu()
            elif choice == "6": self._dashboard()
            elif choice == "0": self.session = None; print("  Logged out."); break
            else: print("  Invalid choice.")

    
    def _add_transaction(self):
        """Inputs and saves a new transaction (Income or Expense)."""
        print("\n── Add Transaction ────────────────────────────────")
        cats = self.category.get_categories_list(self.user.user_id)
        print(f"  Categories: {', '.join(cats)}")
        try:
            amount      = float(input("  Amount ($)            : ").strip())
            t_type      = input("  Type (income/expense) : ").strip().lower()
            category_id = input("  Category              : ").strip()
            date        = input("  Date (YYYY-MM-DD)     : ").strip()
            description = input("  Description           : ").strip()
            
            # Default to today's date if left empty
            if not date:
                date = datetime.date.today().isoformat()
            
            if not self.category.validate_category(category_id):
                category_id = "general"
                
            saved = self.transaction.create_transaction(
                self.user.user_id, amount, t_type, category_id, date, description
            )
            if saved:
                self.user.update_balance(self.user.user_id, amount, t_type)
                print("  ✓ Transaction saved.")
        except ValueError:
            print("  Invalid input.")

    def _view_transactions(self):
        """Fetches and displays the last 10 transactions for the user."""
        print("\n── Recent Transactions ────────────────────────────")
        txns = [t for t in Storage.load_transactions()
                if t.get("user_id") == self.user.user_id][-10:]
        
        if not txns:
            print("  No transactions found.")
            return
            
        print(f"\n  {'Date':<12} {'Type':<8} {'Category':<12} {'Amount':>10}  Description")
        print("  " + "─" * 62)
        for t in txns:
            sign = "+" if t.get("type") == "income" else "-"
            print(f"  {t.get('date','?'):<12} {t.get('type','?'):<8} "
                  f"{t.get('category_id','?'):<12} {sign}${float(t.get('amount',0)):>8.2f}  "
                  f"{t.get('description','')}")

    
    def _budget_menu(self):
        """Sub-menu for budget-specific actions."""
        while True:
            print("\n── Budget Menu ────────────────────────────────────")
            print("  1. Create Budget")
            print("  2. View Budgets")
            print("  0. Back")
            choice = input("  → ").strip()
            if   choice == "1": self._create_budget()
            elif choice == "2": self._view_budgets()
            elif choice == "0": break

    def _create_budget(self):
        """Takes input to set a spending limit for a specific category."""
        print("\n── Create Budget ──────────────────────────────────")
        cats = self.category.get_categories_list(self.user.user_id)
        print(f"  Categories: {', '.join(cats)}")
        try:
            category_id = input("  Category                : ").strip().lower()
            limit       = float(input("  Limit ($)               : ").strip())
            period      = input("  Period (monthly/weekly): ").strip().lower()
            alert       = float(input("  Alert at (%)            : ").strip())
            
            if not self.budget.validate_budget_data(limit, period, alert):
                return
                
            self.budget.create_budget(self.user.user_id, category_id, limit, period, alert)
            print("  ✓ Budget created.")
        except ValueError:
            print("  Invalid input.")

    def _view_budgets(self):
        """Displays all user budgets with real-time spending and remaining balance."""
        budgets = self.budget.get_all_budgets(self.user.user_id)
        if not budgets:
            print("  No budgets found.")
            return
            
        print(f"\n  {'Category':<14} {'Limit':>8} {'Spent':>8} {'Remaining':>10} {'Period':<10} {'Alert%':>7}")
        print("  " + "─" * 60)
        for b in budgets:
            spent     = self.budget.get_current_spending(self.user.user_id, b["category_id"])
            remaining = self.budget.calculate_remaining(b["limit"], spent)
            print(f"  {b['category_id']:<14} ${b['limit']:>7.2f} ${spent:>7.2f} ${remaining:>9.2f} "
                  f"{b['period']:<10} {b['alert']:>6.0f}%")

    
    def _goals_menu(self):
        """Sub-menu for managing financial goals."""
        while True:
            print("\n── Goals Menu ─────────────────────────────────────")
            print("  1. Create Goal")
            print("  2. Contribute to a Goal")
            print("  3. View All Goals")
            print("  0. Back")
            choice = input("  → ").strip()
            if   choice == "1": self._create_goal()
            elif choice == "2": self._contribute_goal()
            elif choice == "3": self.goal_manager.list_goals(self.user.user_id)
            elif choice == "0": break

    def _create_goal(self):
        """Creates a new saving target with a deadline."""
        print("\n── Create Goal ────────────────────────────────────")
        try:
            name     = input("  Goal name         : ").strip()
            target   = float(input("  Target ($)        : ").strip())
            deadline = input("  Deadline (YYYY-MM): ").strip()
            initial  = float(input("  Initial ($, 0)    : ").strip() or "0")
            self.goal_manager.create_goal(self.user.user_id, name, target, deadline, initial)
        except ValueError:
            print("  Invalid input.")

    def _contribute_goal(self):
        """Add funds to an existing goal by ID."""
        print("\n── Contribute to Goal ─────────────────────────────")
        self.goal_manager.list_goals(self.user.user_id)
        goal_id = input("  Goal ID : ").strip()
        try:
            amount = float(input("  Amount ($): ").strip())
            self.goal_manager.contribute(self.user.user_id, goal_id, amount)
        except ValueError:
            print("  Invalid amount.")

    
    def _reports_menu(self):
        """Generates financial summaries or detailed lists within a date range."""
        print("\n── Reports ────────────────────────────────────────")
        print("  Format: YYYY-MM-DD")
        start  = input("  Start date : ").strip()
        end    = input("  End    date : ").strip()
        r_type = input("  Type (summary/detailed): ").strip() or "summary"
        
        txns   = [t for t in Storage.load_transactions()
                  if t.get("user_id") == self.user.user_id
                  and start <= t.get("date", "") <= end]
                  
        self.report.request_report(self.user.user_id, start, end, r_type)
        
        if not txns:
            print(f"  No transactions found between {start} and {end}.")
            return
            
        income  = self.report.calculate_total_income(txns)
        expense = self.report.calculate_total_expense(txns)
        
        print(f"\n  {'─'*40}")
        print(f"  Transactions  : {len(txns)}")
        print(f"  Total Income  : +${income:.2f}")
        print(f"  Total Expense : -${expense:.2f}")
        print(f"  Net           :  ${income - expense:+.2f}")
        print(f"  {'─'*40}")
        
        if r_type == "detailed":
            print(f"\n  {'Date':<12} {'Type':<8} {'Category':<12} {'Amount':>10}  Description")
            print("  " + "─" * 62)
            for t in txns:
                sign = "+" if t.get("type") == "income" else "-"
                print(f"  {t.get('date','?'):<12} {t.get('type','?'):<8} "
                      f"{t.get('category_id','?'):<12} {sign}${float(t.get('amount',0)):>8.2f}  "
                      f"{t.get('description','')}")

    
    def _dashboard(self):
        """A quick overview of finances, goals, and recent activities."""
        print("\n── Dashboard ──────────────────────────────────────")
        txns    = [t for t in Storage.load_transactions() if t.get("user_id") == self.user.user_id]
        goals   = [g for g in Storage.load_goals()        if g.get("user_id") == self.user.user_id]
        budgets = self.budget.get_all_budgets(self.user.user_id)

        income  = sum(float(t.get("amount", 0)) for t in txns if t.get("type") == "income")
        expense = sum(float(t.get("amount", 0)) for t in txns if t.get("type") == "expense")
        balance = self.user.get_user_balance(self.user.user_id)

        print(f"\n  {'─'*40}")
        print(f"  💰 Balance       : ${balance:.2f}")
        print(f"  📈 Total Income  : +${income:.2f}")
        print(f"  📉 Total Expense : -${expense:.2f}")
        print(f"  📋 Budgets       : {len(budgets)} active")
        done = sum(1 for g in goals if g.get("completed"))
        print(f"  🎯 Goals         : {len(goals)} total ({done} completed)")
        print(f"  {'─'*40}")

        recent = txns[-5:]
        if recent:
            print("\n  Last 5 Transactions:")
            for t in reversed(recent):
                sign = "+" if t.get("type") == "income" else "-"
                print(f"  {t.get('date','?')}  {sign}${float(t.get('amount',0)):.2f}  {t.get('description','')}")
        else:
            print("\n  No transactions yet.")
