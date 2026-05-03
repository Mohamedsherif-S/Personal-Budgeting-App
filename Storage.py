import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def _path(filename):
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, filename)

def save(filename, data):
    with open(_path(filename), "w") as f:
        json.dump(data, f, indent=4)

def load(filename, default=None):
    p = _path(filename)
    if not os.path.exists(p):
        return default if default is not None else {}
    with open(p) as f:
        return json.load(f)

def save_users(users):         save("users.json",         users)
def load_users():              return load("users.json",          default={})
def save_transactions(txns):   save("transactions.json",  txns)
def load_transactions():       return load("transactions.json",   default=[])
def save_budgets(budgets):     save("budgets.json",       budgets)
def load_budgets():            return load("budgets.json",        default=[])
def save_goals(goals):         save("goals.json",         goals)
def load_goals():              return load("goals.json",          default=[])
def save_notifications(n):     save("notifications.json", n)
def load_notifications():      return load("notifications.json",  default=[])