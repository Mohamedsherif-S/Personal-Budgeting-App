import Storage


class Transaction:
    def create_transaction(self, user_id, amount, t_type, category_id, date, description, external_id=None):
        if self._validate_transaction(amount, t_type):
            self._save_transaction(user_id, amount, t_type, category_id, date, description, external_id)
            return True
        return False

    def _validate_transaction(self, amount, t_type):
        if amount <= 0:
            print("  Amount must be greater than 0.")
            return False
        if t_type not in ("income", "expense"):
            print("  Type must be 'income' or 'expense'.")
            return False
        return True

    def _save_transaction(self, user_id, amount, t_type, category_id, date, description, external_id=None):
        txns = Storage.load_transactions()
        txns.append({
            "user_id":     user_id,
            "amount":      float(amount),
            "type":        t_type,
            "category_id": category_id,
            "date":        date,
            "description": description,
            "external_id": external_id,
        })
        Storage.save_transactions(txns)
        print("  [Transaction] Saved.")

    def get_recent_transactions(self, user_id, limit):
        txns = Storage.load_transactions()
        return [t for t in txns if t.get("user_id") == user_id][-limit:]

    def get_transactions_by_date_range(self, user_id, start, end):
        txns = Storage.load_transactions()
        return [t for t in txns
                if t.get("user_id") == user_id
                and start <= t.get("date", "") <= end]

    def check_duplicate_transaction(self, user_id, external_id):
        if not external_id:
            return False
        txns = Storage.load_transactions()
        return any(
            t.get("external_id") == external_id and t.get("user_id") == user_id
            for t in txns
        )
