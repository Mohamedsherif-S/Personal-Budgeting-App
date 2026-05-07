import Storage

class Transaction:
    """Handles core transaction operations like creating, validating, and fetching records."""

    def create_transaction(self, user_id, amount, t_type, category_id, date, description, external_id=None):
        """
        Validates and saves a new transaction. 
        Returns True if successful, False otherwise.
        """
        if self._validate_transaction(amount, t_type):
            self._save_transaction(user_id, amount, t_type, category_id, date, description, external_id)
            return True
        return False

    def _validate_transaction(self, amount, t_type):
        """Internal helper to ensure amount is positive and type is correct."""
        if amount <= 0:
            print("  Amount must be greater than 0.")
            return False
        if t_type not in ("income", "expense"):
            print("  Type must be 'income' or 'expense'.")
            return False
        return True

    def _save_transaction(self, user_id, amount, t_type, category_id, date, description, external_id=None):
        """Writes the transaction data to the storage file."""
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
        """Returns the last 'N' transactions for a specific user."""
        txns = Storage.load_transactions()
        return [t for t in txns if t.get("user_id") == user_id][-limit:]

    def get_transactions_by_date_range(self, user_id, start, end):
        """Fetches transactions that fall between the start and end dates."""
        txns = Storage.load_transactions()
        return [t for t in txns
                if t.get("user_id") == user_id
                and start <= t.get("date", "") <= end]

    def check_duplicate_transaction(self, user_id, external_id):
        """
        Checks if a transaction with the same external_id already exists 
        to avoid redundant entries.
        """
        if not external_id:
            return False
        txns = Storage.load_transactions()
        return any(
            t.get("external_id") == external_id and t.get("user_id") == user_id
            for t in txns
        )
