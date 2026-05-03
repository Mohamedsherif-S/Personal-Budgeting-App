import hashlib
import re
import Storage

class User:
    def __init__(self, user_id, username, email, password, phone):
        self.user_id  = user_id
        self.username = username
        self.email    = email
        self.password = password
        self.phone    = phone
        self.balance  = 0.0

    def register(self, username, email, password, phone, admin):
        if not self.validate_user_data(email, username):
            return False
        users = Storage.load_users()
        for data in users.values():
            if data.get("email") == email:
                print("  Email already registered.")
                return False
        self.user_id  = f"U{len(users)+1:03d}"
        self.username = username
        self.email    = email
        self.password = self.hash_password(password)
        self.phone    = phone
        self.balance  = 0.0
        users[self.user_id] = self._to_dict()
        Storage.save_users(users)
        admin.notify_new_user(self.user_id, "today")
        print("  [User] Registration successful.")
        return True

    def validate_user_data(self, email, username):
        if len(username) < 3:
            print("  Username must be at least 3 characters.")
            return False
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            print("  Invalid email format.")
            return False
        return True

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, email, password):
        if self.email != email or self.password != self.hash_password(password):
            print("  [User] Wrong credentials.")
            return None
        self.balance = self.get_user_balance(self.user_id)
        print("  [User] Login successful.")
        return f"session_{self.user_id}"

    def get_user_balance(self, user_id):
        users = Storage.load_users()
        return users.get(user_id, {}).get("balance", 0.0)

    def update_balance(self, user_id, amount, t_type):
        if t_type == "income":
            self.balance += amount
        else:
            self.balance -= amount
        users = Storage.load_users()
        if user_id in users:
            users[user_id]["balance"] = self.balance
            Storage.save_users(users)
        print(f"  [User] Balance → ${self.balance:.2f}")

    def _to_dict(self):
        return {
            "user_id":  self.user_id,
            "username": self.username,
            "email":    self.email,
            "password": self.password,
            "phone":    self.phone,
            "balance":  self.balance
        }

    def get_user_data(self, user_id):
        return self._to_dict()

    def verify_user_access(self, user_id):
        return self.user_id == user_id

    def check_existing_budget(self, user_id, category_id, period):
        return False

    def initiate_bank_sync(self, user_id, bank_id):
        print(f"  [User] Bank sync started: {bank_id}")

    def update_last_sync_date(self, user_id, bank_id, current_time):
        users = Storage.load_users()
        if user_id in users:
            users[user_id]["last_sync"] = str(current_time)
            Storage.save_users(users)

    def initiate_transaction(self, user_id):
        print(f"  [User] Transaction flow started.")

    def initiate_budget_creation(self, user_id):
        print(f"  [User] Budget creation flow started.")

    def generate_session(self, user_id):
        return f"session_{user_id}"