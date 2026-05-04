import Storage


class Budget:
    def create_budget(self, user_id, category_id, limit, period, alert):
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
        return [b for b in Storage.load_budgets() if b.get("user_id") == user_id]

    def get_current_spending(self, user_id, category_id):
        txns = Storage.load_transactions()
        return sum(
            float(t.get("amount", 0))
            for t in txns
            if t.get("user_id") == user_id
            and t.get("category_id") == category_id
            and t.get("type") == "expense"
        )

    def calculate_remaining(self, limit, current):
        return limit - current