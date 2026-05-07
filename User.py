import hashlib
import re
import Storage

class User:
    """
    Handles user account logic including registration, authentication, 
    and balance management.
    """
    def __init__(self, user_id, username, email, password, phone):
        """Initializes a user instance with basic profile information."""
        self.user_id  = user_id
        self.username = username
        self.email    = email
        self.password = password
        self.phone    = phone
        self.balance  = 0.0
    
    def register(self, username, email, password, phone, admin):
        """
        Processes new user registration. 
        Checks for existing emails and hashes the password before saving.
        """
        if not self._validate_user_data(email, username):
            return False
            
        users = Storage.load_users()
        # Check if the email is already taken
        for data in users.values():
            if data.get("email") == email:
                print("  Email already registered.")
                return False
        
        # Generate a new ID based on current user count
        self.user_id  = f"U{len(users)+1:03d}"
        self.username = username
        self.email    = email
        self.password = self._hash_password(password)
        self.phone    = phone
        self.balance  = 0.0
        
        users[self.user_id] = self._to_dict()
        Storage.save_users(users)
        
        # Notify admin module about the new registration
        admin.notify_new_user(self.user_id, "today")
        print("  [User] Registration successful.")
        return True

    def _validate_user_data(self, email, username):
        """Internal check for username length and email format using Regex."""
        if len(username) < 3:
            print("  Username must be at least 3 characters.")
            return False
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            print("  Invalid email format.")
            return False
        return True

    def _hash_password(self, password):
        """Secures the password using SHA-256 hashing."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def find_by_email(self, email):
        """Searches the database for a user matching the provided email."""
        users = Storage.load_users()
        return next((d for d in users.values() if d.get("email") == email), None)

    def load_from_dict(self, data):
        """Populates the current object attributes from a dictionary (e.g., from JSON)."""
        self.user_id  = data["user_id"]
        self.username = data["username"]
        self.email    = data["email"]
        self.password = data["password"]
        self.phone    = data.get("phone", "")
        self.balance  = data.get("balance", 0.0)

    def login(self, email, password):
        """
        Verifies credentials and returns a session string if successful.
        Syncs the current balance upon login.
        """
        if self.email != email or self.password != self._hash_password(password):
            print("  [User] Wrong credentials.")
            return None
        self.balance = self.get_user_balance(self.user_id)
        print("  [User] Login successful.")
        return f"session_{self.user_id}"

    
    def get_user_balance(self, user_id):
        """Retrieves the latest balance for a specific user from storage."""
        users = Storage.load_users()
        return float(users.get(user_id, {}).get("balance", 0.0))

    def update_balance(self, user_id, amount, t_type):
        """
        Adjusts the balance based on transaction type (income/expense).
        Persists the change to the users storage file.
        """
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
        """Converts user object attributes into a dictionary for JSON storage."""
        return {
            "user_id":  self.user_id,
            "username": self.username,
            "email":    self.email,
            "password": self.password,
            "phone":    self.phone,
            "balance":  self.balance,
        }

    def generate_session(self, user_id):
        """Helper to create a simple session identifier."""
        return f"session_{user_id}"
