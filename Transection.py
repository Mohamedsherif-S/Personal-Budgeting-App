class Transaction:
    """
    Represents financial transactions.
    """

    def create_transaction(self, user_id, amount, t_type, category_id, date, description, external_id=None):
        if self.validate_transaction(amount, t_type, date):
            self.save_transaction(user_id, amount, t_type, category_id, date, description)
        return True

    def validate_transaction(self, amount, t_type, date):
        return amount > 0

    def save_transaction(self, user_id, amount, t_type, category_id, date, description):
        print("Transaction saved")

    def get_recent_transactions(self, user_id, limit):
        return []

    def fetch_transactions(self, user_id, order_by, limit):
        return []

    def get_transactions_by_date_range(self, user_id, start, end):
        return []

    def filter_transactions(self, user_id, start, end):
        return []

    def get_category_for_transaction(self, transaction_id):
        return None

    def check_duplicate_transaction(self, user_id, external_id, amount, date):
        return False