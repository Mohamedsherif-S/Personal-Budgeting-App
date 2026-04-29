class User:
    """
    Represents a system user.
    """

    def __init__(self, user_id, username, email, password, phone):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.balance = 0.0

    def register(self, username, email, password, phone, admin):
        """
        Handles full registration flow.
        """
        if not self.validate_user_data(email, username):
            print("Invalid data")
            return False

        hashed = self.hash_password(password)
        created = self.create_account(username, email, hashed, phone)

        if created:
            admin.notify_new_user(self.user_id, "today")
            print("Registration successful")

        return created

    def validate_user_data(self, email, username):
        """Validates user data."""
        return "@" in email and len(username) > 2

    def hash_password(self, password):
        """Hashes password."""
        return hash(password)

    def create_account(self, username, email, hashed_password, phone):
        self.username = username
        self.email = email
        self.password = hashed_password
        self.phone = phone
        return True

    def login(self, email, password):
        """
        Handles login flow.
        """
        if not self.validate_credentials(email, password):
            print("Login failed")
            return None

        session = self.generate_session(self.user_id)
        balance = self.get_user_balance(self.user_id)

        print("Login successful")
        return session
    def validate_credentials(self, email, password):
        """Validates login."""
        return self.email == email and self.password == hash(password)

    def generate_session(self, user_id):
        """Generates session."""
        return f"session_{user_id}"

    def get_user_balance(self, user_id):
        """Returns balance."""
        return self.balance

    def update_balance(self, user_id, amount, t_type):
        """Updates balance."""
        if t_type == "income":
            self.balance += amount
        else:
            self.balance -= amount

    def initiate_transaction(self, user_id):
        print("Transaction started")

    def initiate_budget_creation(self, user_id):
        print("Budget creation started")

    def check_existing_budget(self, user_id, category_id, period):
        return False

    def get_user_data(self, user_id):
        return self.__dict__

    def verify_user_access(self, user_id):
        return True

    def initiate_bank_sync(self, user_id, bank_id):
        print("Sync started")

    def update_last_sync_date(self, user_id, bank_id, current_time):
        print("Sync date updated")