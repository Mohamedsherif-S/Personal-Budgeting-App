import datetime
import Storage

class BankSync:
    def __init__(self, user, external_bank, transaction, category, budget, notification):
        self.user         = user
        self.bank         = external_bank
        self.transaction  = transaction
        self.category     = category
        self.budget       = budget
        self.notification = notification

    def sync(self, user_id, bank_id, credentials):
        print("\n── Bank Sync ──────────────────────────────────────")
        self.user.initiate_bank_sync(user_id, bank_id)

        if not self.bank.request_connection(user_id, bank_id, credentials):
            print("  Connection failed.")
            return 0

        token = self.bank.authenticate(credentials)
        if not token:
            print("  Authentication failed.")
            return 0

        last_sync = Storage.load_users().get(user_id, {}).get("last_sync", "2000-01-01")
        raw_list  = self.bank.request_transactions(token, last_sync)
        print(f"  Fetched {len(raw_list)} transactions from bank.")

        new_count = sum(self._process(user_id, raw) for raw in raw_list)
        self.user.update_last_sync_date(user_id, bank_id, datetime.datetime.now().isoformat())
        print(f"  Sync complete — {new_count} new transaction(s) imported.")
        return new_count

    def _process(self, user_id, raw):
        ext_id      = raw.get("external_id")
        amount      = raw.get("amount", 0)
        t_type      = raw.get("type", "expense")
        description = raw.get("description", "")
        merchant    = raw.get("merchant", "")
        date        = raw.get("date", datetime.date.today().isoformat())

        if self.transaction.check_duplicate_transaction(user_id, ext_id, amount, date):
            print(f"  Skipping duplicate: {ext_id}")
            return 0

        category_id = self.category.auto_map_category(description, merchant)
        self.transaction.create_transaction(user_id, amount, t_type, category_id, date, description, ext_id)
        self.user.update_balance(user_id, amount, t_type)

        if not self.budget.check_budget_limit(user_id, category_id, amount):
            self.notification.create_notification(user_id, "budget_alert", category_id, {"amount": amount})
        else:
            self.notification.create_notification(user_id, "transaction_synced", ext_id, {"amount": amount})
        return 1