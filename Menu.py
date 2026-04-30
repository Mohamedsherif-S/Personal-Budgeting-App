"""
Menu.py — Console menu system.

Responsibilities:
  • Display menus and collect user input.
  • Delegate ALL business logic to the appropriate class/orchestrator.
  • Never implement logic directly here.
"""


class Menu:
    """
    Drives the console UI.
    Receives pre-built orchestrator objects via the constructor
    so it stays decoupled from object creation.
    """

    def __init__(self, user, bank_sync, goal_manager, transaction,
                 budget, report, dashboard, category):
        self.user         = user
        self.bank_sync    = bank_sync
        self.goal_manager = goal_manager
        self.transaction  = transaction
        self.budget       = budget
        self.report       = report
        self.dashboard    = dashboard
        self.category     = category
        self.session      = None   # Set after login

    # ─────────────────────────────────────────────────────────────────────────
    #  Top-level menus
    # ─────────────────────────────────────────────────────────────────────────

    def show_welcome(self):
        """First screen the user sees."""
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
            elif choice == "0":
                print("\n  Goodbye! 👋\n")
                break
            else:
                print("  Invalid choice — try again.")

    def show_main_menu(self):
        """Main dashboard after login."""
        while True:
            balance = self.user.get_user_balance(self.user.user_id)
            print(f"\n{'═'*45}")
            print(f"  Welcome, {self.user.username}  |  Balance: ${balance:.2f}")
            print("═" * 45)
            print("  1. Add Transaction")
            print("  2. View Transactions")
            print("  3. Manage Budgets")
            print("  4. Goals              (US-7)")
            print("  5. Sync Bank Account  (US-6)")
            print("  6. Reports")
            print("  7. Dashboard")
            print("  0. Logout")
            print("─" * 45)

            choice = input("  → ").strip()

            if   choice == "1": self._add_transaction()
            elif choice == "2": self._view_transactions()
            elif choice == "3": self._budget_menu()
            elif choice == "4": self._goals_menu()
            elif choice == "5": self._bank_sync_menu()
            elif choice == "6": self._reports_menu()
            elif choice == "7": self._dashboard()
            elif choice == "0":
                self.session = None
                print("  Logged out.")
                break
            else:
                print("  Invalid choice.")

    # ─────────────────────────────────────────────────────────────────────────
    #  Auth screens
    # ─────────────────────────────────────────────────────────────────────────

    def _register(self):
        print("\n── Register ───────────────────────────────────────")
        username = input("  Username : ").strip()
        email    = input("  Email    : ").strip()
        password = input("  Password : ").strip()
        phone    = input("  Phone    : ").strip()

        from Admin import Admin
        admin = Admin()

        # Delegate to User class (preserves sequence diagram traceability)
        success = self.user.register(username, email, password, phone, admin)
        if success:
            print("  ✓ Account created! Please login.")

    def _login(self):
        print("\n── Login ──────────────────────────────────────────")
        email    = input("  Email    : ").strip()
        password = input("  Password : ").strip()

        self.session = self.user.login(email, password)
        if self.session:
            self.show_main_menu()

    # ─────────────────────────────────────────────────────────────────────────
    #  Transaction screen
    # ─────────────────────────────────────────────────────────────────────────

    def _add_transaction(self):
        print("\n── Add Transaction ────────────────────────────────")
        self.user.initiate_transaction(self.user.user_id)

        categories = self.category.get_categories_list(self.user.user_id)
        print(f"  Available categories: {', '.join(categories)}")

        try:
            amount      = float(input("  Amount      : $").strip())
            t_type      = input("  Type (income/expense): ").strip().lower()
            category_id = input("  Category    : ").strip()
            date        = input("  Date (YYYY-MM-DD, Enter=today): ").strip()
            description = input("  Description : ").strip()

            if not date:
                import datetime
                date = datetime.date.today().isoformat()

            if not self.category.validate_category(category_id):
                category_id = "general"

            # Delegate to Transaction class (sequence diagram traceability)
            saved = self.transaction.create_transaction(
                self.user.user_id, amount, t_type, category_id, date, description
            )

            if saved:
                # Update balance via User class
                self.user.update_balance(self.user.user_id, amount, t_type)
                # Check budget (via Budget class)
                ok = self.budget.check_budget_limit(
                    self.user.user_id, category_id, amount
                )
                if not ok:
                    print("  ⚠  You have exceeded your budget for this category!")
                print("  ✓ Transaction saved.")
        except ValueError:
            print("  Invalid input — transaction cancelled.")

    def _view_transactions(self):
        print("\n── Recent Transactions ────────────────────────────")
        txns = self.transaction.get_recent_transactions(self.user.user_id, limit=10)
        if not txns:
            # Fall back to persisted data
            import Storage
            all_txns = Storage.load_transactions()
            txns = [t for t in all_txns if t["user_id"] == self.user.user_id][-10:]

        if not txns:
            print("  No transactions found.")
            return

        print(f"\n  {'Date':<12} {'Type':<8} {'Category':<12} {'Amount':>9} Description")
        print("  " + "─" * 60)
        for t in txns:
            sign = "+" if t.get("type") == "income" else "-"
            print(f"  {t.get('date','?'):<12} {t.get('type','?'):<8} "
                  f"{t.get('category_id','?'):<12} {sign}${t.get('amount',0):>8.2f} "
                  f"{t.get('description','')}")

    # ─────────────────────────────────────────────────────────────────────────
    #  Budget screen
    # ─────────────────────────────────────────────────────────────────────────

    def _budget_menu(self):
        while True:
            print("\n── Budget Menu ────────────────────────────────────")
            print("  1. Create Budget")
            print("  2. View Budgets")
            print("  0. Back")
            choice = input("  → ").strip()

            if choice == "1":
                self._create_budget()
            elif choice == "2":
                self._view_budgets()
            elif choice == "0":
                break

    def _create_budget(self):
        print("\n── Create Budget ──────────────────────────────────")
        self.user.initiate_budget_creation(self.user.user_id)
        categories = self.category.get_categories_list(self.user.user_id)
        print(f"  Categories: {', '.join(categories)}")

        try:
            category_id = input("  Category  : ").strip()
            limit       = float(input("  Limit ($) : ").strip())
            period      = input("  Period (monthly/weekly): ").strip()
            alert       = float(input("  Alert at (%, e.g. 80): ").strip())

            # Check for duplicates via User class
            exists = self.user.check_existing_budget(
                self.user.user_id, category_id, period
            )
            if exists:
                print("  A budget for this category/period already exists.")
                return

            # Delegate to Budget class
            self.budget.create_budget(
                self.user.user_id, category_id, limit, period, alert
            )

            # Persist
            import Storage
            budgets = Storage.load_budgets()
            if isinstance(budgets, dict):
                budgets = list(budgets.values())
            budgets.append({
                "user_id": self.user.user_id,
                "category_id": category_id,
                "limit": limit,
                "period": period,
                "alert": alert
            })
            Storage.save_budgets(budgets)
            print("  ✓ Budget created.")
        except ValueError:
            print("  Invalid input.")

    def _view_budgets(self):
        import Storage
        budgets = [b for b in Storage.load_budgets()
                   if b["user_id"] == self.user.user_id]
        if not budgets:
            print("  No budgets found.")
            return

        print(f"\n  {'Category':<14} {'Limit':>8} {'Period':<10} {'Alert%':>7}")
        print("  " + "─" * 44)
        for b in budgets:
            print(f"  {b['category_id']:<14} ${b['limit']:>7.2f} {b['period']:<10} {b['alert']:>6.0f}%")

    # ─────────────────────────────────────────────────────────────────────────
    #  Goals screen (US-7)
    # ─────────────────────────────────────────────────────────────────────────

    def _goals_menu(self):
        while True:
            print("\n── Goals Menu ─────────────────────────────────────")
            print("  1. Create New Goal")
            print("  2. Contribute to a Goal")
            print("  3. View All Goals")
            print("  0. Back")
            choice = input("  → ").strip()

            if   choice == "1": self._create_goal()
            elif choice == "2": self._contribute_goal()
            elif choice == "3": self.goal_manager.list_goals(self.user.user_id)
            elif choice == "0": break

    def _create_goal(self):
        print("\n── Create Goal ────────────────────────────────────")
        try:
            name     = input("  Goal name        : ").strip()
            target   = float(input("  Target amount ($): ").strip())
            deadline = input("  Deadline (YYYY-MM): ").strip()
            initial  = float(input("  Initial deposit ($, Enter=0): ").strip() or "0")

            # Delegate to GoalManager (which calls Goal class methods)
            self.goal_manager.create_goal(
                self.user.user_id, name, target, deadline, initial
            )
        except ValueError:
            print("  Invalid input.")

    def _contribute_goal(self):
        print("\n── Contribute to Goal ─────────────────────────────")
        self.goal_manager.list_goals(self.user.user_id)
        goal_id = input("  Enter Goal ID: ").strip()
        try:
            amount = float(input("  Amount ($)   : ").strip())
            self.goal_manager.contribute(self.user.user_id, goal_id, amount)
        except ValueError:
            print("  Invalid amount.")

    # ─────────────────────────────────────────────────────────────────────────
    #  Bank Sync screen (US-6)
    # ─────────────────────────────────────────────────────────────────────────

    def _bank_sync_menu(self):
        print("\n── Sync External Bank ─────────────────────────────")
        bank_id  = input("  Bank ID (e.g. BANK001): ").strip()
        username = input("  Bank username          : ").strip()
        password = input("  Bank password          : ").strip()

        credentials = {"username": username, "password": password}

        # Delegate to BankSync orchestrator (which calls all sequence-diagram methods)
        count = self.bank_sync.sync(self.user.user_id, bank_id, credentials)
        print(f"  ✓ {count} new transaction(s) imported from bank.")

    # ─────────────────────────────────────────────────────────────────────────
    #  Reports screen
    # ─────────────────────────────────────────────────────────────────────────

    def _reports_menu(self):
        print("\n── Reports ────────────────────────────────────────")
        start  = input("  Start date (YYYY-MM-DD): ").strip()
        end    = input("  End   date (YYYY-MM-DD): ").strip()
        r_type = input("  Type (summary/detailed): ").strip()

        self.report.request_report(self.user.user_id, start, end, r_type)

        # Use persisted transactions for a real summary
        import Storage
        txns = [t for t in Storage.load_transactions()
                if t["user_id"] == self.user.user_id
                and start <= t.get("date", "") <= end]

        total_income  = self.report.calculate_total_income(txns)
        total_expense = self.report.calculate_total_expense(txns)
        print(f"\n  Total Income  : ${total_income:.2f}")
        print(f"  Total Expense : ${total_expense:.2f}")
        print(f"  Net           : ${total_income - total_expense:.2f}")

    # ─────────────────────────────────────────────────────────────────────────
    #  Dashboard screen
    # ─────────────────────────────────────────────────────────────────────────

    def _dashboard(self):
        print("\n── Dashboard ──────────────────────────────────────")
        self.dashboard.load_dashboard(self.user.user_id)

        import Storage
        txns    = [t for t in Storage.load_transactions()
                   if t["user_id"] == self.user.user_id]
        goals   = [g for g in Storage.load_goals()
                   if g["user_id"] == self.user.user_id]
        budgets = [b for b in Storage.load_budgets()
                   if b["user_id"] == self.user.user_id]

        income  = sum(t["amount"] for t in txns if t["type"] == "income")
        expense = sum(t["amount"] for t in txns if t["type"] == "expense")

        print(f"  Balance  : ${self.user.balance:.2f}")
        print(f"  Income   : ${income:.2f}")
        print(f"  Expenses : ${expense:.2f}")
        print(f"  Budgets  : {len(budgets)} active")
        completed = sum(1 for g in goals if g["completed"])
        print(f"  Goals    : {len(goals)} total  ({completed} completed)")