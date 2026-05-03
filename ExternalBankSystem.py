import datetime

class ExternalBankSystem:
    def request_connection(self, user_id, bank_id, credentials):
        return True

    def authenticate(self, credentials):
        return "token_ok"

    def validate_api_access(self, user_id, bank_id):
        return True

    def request_transactions(self, token, last_sync):
        today = datetime.date.today().isoformat()
        return [
            {"external_id": "EXT001", "amount": 1500.0, "type": "income",
             "description": "Salary deposit",   "merchant": "Employer",    "date": today},
            {"external_id": "EXT002", "amount": 45.0,   "type": "expense",
             "description": "Grocery shopping", "merchant": "Supermarket", "date": today},
            {"external_id": "EXT003", "amount": 120.0,  "type": "expense",
             "description": "Electricity bill", "merchant": "Utility Co",  "date": today},
        ]

    def fetch_transactions(self, account_id, from_date):
        return []