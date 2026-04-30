"""
User.py — Represents a system user.
Extended to persist user data via Storage.py.
"""

import Storage


class User:
    """
    Represents a system user.
    Handles registration, login, balance, and sync triggers.
    """

    def __init__(self, user_id, username, email, password, phone):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password  # stored as hash
        self.phone = phone
        self.balance = 0.0

    # ── Registration ──────────────────────────────────────────────────────────

    def register(self, username, email, password, phone, admin):
        """Handles full registration flow (sequence diagram US-1)."""
        if not self.validate_user_data(email, username):
            print("  [User] Invalid data — registration aborted.")
            return False

        hashed = self.hash_password(password)
        created = self.create_account(username, email, hashed, phone)

        if created:
            # Persist the new user immediately
            users = Storage.load_users()
            users[self.user_id] = self.get_user_data(self.user_id)
            Storage.save_users(users)

            admin.notify_new_user(self.user_id, "today")
            print("  [User] Registration successful.")

        return created

    def validate_user_data(self, email, username):
        """Email must contain '@' and username must be > 2 chars."""
        return "@" in email and len(username) > 2

    def hash_password(self, password):
        """Simple hash — in production use bcrypt or similar."""
        return str(hash(password))

    def create_account(self, username, email, hashed_password, phone):
        """Stores validated data on the object."""
        self.username = username
        self.email = email
        self.password = hashed_password
        self.phone = phone
        return True

    # ── Login ─────────────────────────────────────────────────────────────────

    def login(self, email, password):
        """Handles login flow; returns session token or None."""
        if not self.validate_credentials(email, password):
            print("  [User] Login failed — wrong credentials.")
            return None

        session = self.generate_session(self.user_id)
        self.balance = self.get_user_balance(self.user_id)
        print("  [User] Login successful.")
        return session

    def validate_credentials(self, email, password):
        """Check email + hashed password match."""
        return self.email == email and self.password == str(hash(password))

    def generate_session(self, user_id):
        """Produce a simple session string."""
        return f"session_{user_id}"

    # ── Balance ───────────────────────────────────────────────────────────────

    def get_user_balance(self, user_id):
        """Load balance from persisted data (falls back to in-memory)."""
        users = Storage.load_users()
        if user_id in users:
            return users[user_id].get("balance", self.balance)
        return self.balance

    def update_balance(self, user_id, amount, t_type):
        """
        Adjusts balance for income or expense.
        Called after every transaction is saved.
        """
        if t_type == "income":
            self.balance += amount
        else:
            self.balance -= amount

        # Persist updated balance
        users = Storage.load_users()
        if user_id in users:
            users[user_id]["balance"] = self.balance
            Storage.save_users(users)

        print(f"  [User] Balance updated → ${self.balance:.2f}")

    # ── Utility ───────────────────────────────────────────────────────────────

    def get_user_data(self, user_id):
        """Return a serialisable dict of this user's data."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "balance": self.balance
        }

    def verify_user_access(self, user_id):
        return self.user_id == user_id

    def check_existing_budget(self, user_id, category_id, period):
        """Checks in-memory; real impl would query DB/file."""
        return False

    # ── Bank sync triggers ────────────────────────────────────────────────────

    def initiate_bank_sync(self, user_id, bank_id):
        """Entry point for User Story 6 — starts the sync flow."""
        print(f"  [User] Initiating bank sync for user '{user_id}', bank '{bank_id}'...")

    def update_last_sync_date(self, user_id, bank_id, current_time):
        """Records when the last successful sync happened."""
        users = Storage.load_users()
        if user_id in users:
            users[user_id]["last_sync"] = str(current_time)
            Storage.save_users(users)
        print(f"  [User] Sync date updated to {current_time}.")

    # ── Other triggers (keep for traceability) ────────────────────────────────

    def initiate_transaction(self, user_id):
        print(f"  [User] Transaction flow started for '{user_id}'.")

    def initiate_budget_creation(self, user_id):
        print(f"  [User] Budget creation flow started for '{user_id}'.")