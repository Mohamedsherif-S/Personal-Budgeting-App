import Storage

class Budget:
    # This class handles everything related to user budgets
    def create_budget(self, user_id, category_id, limit, period, alert):
        """Creates a new budget and saves it to the storage file."""
        budgets = Storage.load_budgets()
        budgets.append({
            "user_id":     user_id,
            "category_id": category_id,
            "limit":       float(limit),
            "period":      period.strip().lower(),
            "alert":       float(alert),
        })
        Storage.save_budgets(budgets)
        return True

    def validate_budget_data(self, limit, period, alert):
        """Checks if the input data (limit, period, alert) is valid."""
        if limit <= 0:
            print("  Limit must be greater than 0.")
            return False
        if period.strip().lower() not in ("monthly", "weekly"):
            print("  Period must be 'monthly' or 'weekly'.")
            return False
        if not (0 < alert <= 100):
            print("  Alert must be between 1 and 100.")
            return False
        return True

    def get_all_budgets(self, user_id):
        """Returns a list of all budgets for a specific user."""
        return [b for b in Storage.load_budgets() if b.get("user_id") == user_id]

    def get_current_spending(self, user_id, category_id):
        """Calculates total expense spending for a user in a specific category."""
        txns = Storage.load_transactions()
        return sum(
            float(t.get("amount", 0))
            for t in txns
            if t.get("user_id") == user_id
            and t.get("category_id") == category_id
            and t.get("type") == "expense"
        )

    def calculate_remaining(self, limit, current):
        """Simply subtracts current spending from the budget limit."""
        return limit - current
