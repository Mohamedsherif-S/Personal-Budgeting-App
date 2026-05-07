import json
import os

# Define the base directory for data storage
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def _path(filename):
    """
    Helper to ensure the data directory exists and return the full file path.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, filename)

def save(filename, data):
    """
    Writes data to a JSON file with 4-space indentation for readability.
    """
    with open(_path(filename), "w") as f:
        json.dump(data, f, indent=4)

def load(filename, default=None):
    """
    Reads data from a JSON file. Returns a default value if the file doesn't exist.
    """
    p = _path(filename)
    if not os.path.exists(p):
        return default if default is not None else {}
    with open(p) as f:
        return json.load(f)

# --- Specific Wrappers for different data types ---

def save_users(users):         
    """Saves the user database to users.json."""
    save("users.json", users)

def load_users():              
    """Loads all users, returns an empty dict if not found."""
    return load("users.json", default={})

def save_transactions(txns):   
    """Saves the list of transactions to transactions.json."""
    save("transactions.json", txns)

def load_transactions():       
    """Loads all transactions, returns an empty list if not found."""
    return load("transactions.json", default=[])

def save_budgets(budgets):     
    """Saves budget settings to budgets.json."""
    save("budgets.json", budgets)

def load_budgets():            
    """Loads all budgets, returns an empty list if not found."""
    return load("budgets.json", default=[])

def save_goals(goals):         
    """Saves financial goals to goals.json."""
    save("goals.json", goals)

def load_goals():              
    """Loads all goals, returns an empty list if not found."""
    return load("goals.json", default=[])

def save_notifications(n):     
    """Saves notification logs to notifications.json."""
    save("notifications.json", n)

def load_notifications():      
    """Loads all notifications, returns an empty list if not found."""
    return load("notifications.json", default=[])
