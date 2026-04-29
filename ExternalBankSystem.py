class ExternalBankSystem:
    """
    Handles bank integration.
    """

    def request_connection(self, user_id, bank_id, credentials):
        return True

    def authenticate(self, credentials):
        return "token"

    def validate_api_access(self, user_id, bank_id):
        return True

    def request_transactions(self, token, last_sync):
        return []

    def fetch_transactions(self, account_id, from_date):
        return []