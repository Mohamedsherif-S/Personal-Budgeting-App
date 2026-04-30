"""
BankSync.py — Orchestrates User Story 6: Sync External Bank Transactions.

Sequence diagram trace:
  User.initiateBankSync()
    → ExternalBankSystem.requestConnection()
    → ExternalBankSystem.authenticate()
    → ExternalBankSystem.requestTransactions()
    → Transaction.checkDuplicateTransaction()
    → Category.autoMapCategory()
    → Transaction.createTransaction()  → Transaction.saveTransaction()
    → User.updateBalance()
    → Budget.checkBudgetLimit()
    → Notification.createNotification()
"""

import datetime
import Storage


class BankSync:
    """
    Orchestrates the bank-sync flow.
    Delegates to existing classes — does NOT re-implement their logic.
    """

    def __init__(self, user, external_bank, transaction, category, budget, notification):
        # Inject dependencies (all existing class instances)
        self.user = user
        self.bank = external_bank
        self.transaction = transaction
        self.category = category
        self.budget = budget
        self.notification = notification

    # ─────────────────────────────────────────────────────────────────────────
    #  Main entry point
    # ─────────────────────────────────────────────────────────────────────────

    def sync(self, user_id, bank_id, credentials):
        """
        Full sync flow as described in the sequence diagram.
        Returns the number of new transactions imported.
        """
        print("\n── Bank Sync ──────────────────────────────────────")

        # Step 1 — User triggers the sync
        self.user.initiate_bank_sync(user_id, bank_id)

        # Step 2 — Request connection to the external bank
        connected = self.bank.request_connection(user_id, bank_id, credentials)
        if not connected:
            print("  [BankSync] Connection failed — aborting.")
            return 0

        # Step 3 — Authenticate and get an access token
        token = self.bank.authenticate(credentials)
        if not token:
            print("  [BankSync] Authentication failed — aborting.")
            return 0
        print(f"  [BankSync] Authenticated. Token: {token}")

        # Step 4 — Fetch raw transactions from the bank
        last_sync = self._get_last_sync(user_id, bank_id)
        raw_transactions = self.bank.request_transactions(token, last_sync)
        print(f"  [BankSync] Fetched {len(raw_transactions)} transactions from bank.")

        new_count = 0

        for raw in raw_transactions:
            new_count += self._process_one_transaction(user_id, raw)

        # Step 5 — Record sync timestamp
        self.user.update_last_sync_date(user_id, bank_id, datetime.datetime.now().isoformat())

        print(f"  [BankSync] Sync complete — {new_count} new transaction(s) imported.")
        return new_count

    # ─────────────────────────────────────────────────────────────────────────
    #  Private helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _process_one_transaction(self, user_id, raw):
        """
        Process a single raw bank transaction.
        Returns 1 if saved, 0 if duplicate/skipped.
        """
        external_id  = raw.get("external_id")
        amount       = raw.get("amount", 0)
        t_type       = raw.get("type", "expense")   # "income" or "expense"
        description  = raw.get("description", "")
        merchant     = raw.get("merchant", "")
        date         = raw.get("date", datetime.date.today().isoformat())

        # Step A — Duplicate check (sequence diagram)
        is_duplicate = self.transaction.check_duplicate_transaction(
            user_id, external_id, amount, date
        )
        if is_duplicate:
            print(f"  [BankSync] Skipping duplicate: {external_id}")
            return 0

        # Step B — Auto-map category (sequence diagram)
        category_id = self.category.auto_map_category(description, merchant)
        print(f"  [BankSync] Category mapped → '{category_id}' for '{description}'")

        # Step C — Create & save transaction (sequence diagram)
        self.transaction.create_transaction(
            user_id, amount, t_type, category_id, date, description, external_id
        )

        # Persist to JSON storage
        self._persist_transaction(
            user_id, amount, t_type, category_id, date, description, external_id
        )

        # Step D — Update user balance (sequence diagram)
        self.user.update_balance(user_id, amount, t_type)

        # Step E — Check budget limit (sequence diagram)
        over_budget = not self.budget.check_budget_limit(user_id, category_id, amount)
        if over_budget:
            print(f"  [BankSync] ⚠ Budget limit exceeded for category '{category_id}'!")
            # Step F — Notify user of budget breach (sequence diagram)
            self.notification.create_notification(
                user_id,
                n_type="budget_alert",
                ref_id=category_id,
                data={"amount": amount, "description": description}
            )
        else:
            # General sync success notification
            self.notification.create_notification(
                user_id,
                n_type="transaction_synced",
                ref_id=external_id,
                data={"amount": amount, "description": description}
            )

        return 1

    def _persist_transaction(self, user_id, amount, t_type, category_id, date, description, external_id):
        """Save transaction dict to transactions.json."""
        txns = Storage.load_transactions()
        transaction_record = {
            "user_id":     user_id,
            "amount":      amount,
            "type":        t_type,
            "category_id": category_id,
            "date":        date,
            "description": description,
            "external_id": external_id
        }

        if isinstance(txns, dict):
            if "transactions" not in txns or not isinstance(txns["transactions"], list):
                txns["transactions"] = []
            txns["transactions"].append(transaction_record)
        else:
            txns.append(transaction_record)

        Storage.save_transactions(txns)

    def _get_last_sync(self, user_id, bank_id):
        """Retrieve the last sync date for this user+bank (or a safe default)."""
        users = Storage.load_users()
        return users.get(user_id, {}).get("last_sync", "2000-01-01")