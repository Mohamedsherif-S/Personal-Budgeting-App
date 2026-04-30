"""
Storage.py — JSON-based file persistence helper.
Handles saving and loading all app data to/from disk.
"""

import json
import os

# Path to the data directory (created automatically if missing)
DATA_DIR = "data"


def _ensure_data_dir():
    """Create the data/ folder if it doesn't exist yet."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _file_path(filename):
    """Return the full path for a given data file."""
    return os.path.join(DATA_DIR, filename)


# ─────────────────────────────────────────────
#  Generic save / load
# ─────────────────────────────────────────────

def save(filename, data):
    """
    Save any Python dict or list to a JSON file.
    Example: save("users.json", users_dict)
    """
    _ensure_data_dir()
    with open(_file_path(filename), "w") as f:
        json.dump(data, f, indent=4)


def load(filename, default=None):
    """
    Load data from a JSON file.
    Returns `default` (empty dict/list) if the file doesn't exist yet.
    Example: load("users.json", default={})
    """
    path = _file_path(filename)
    if not os.path.exists(path):
        return default if default is not None else {}
    with open(path, "r") as f:
        return json.load(f)


# ─────────────────────────────────────────────
#  Named helpers for each data entity
# ─────────────────────────────────────────────

def save_users(users):
    save("users.json", users)

def load_users():
    return load("users.json", default={})

def save_transactions(txns):
    save("transactions.json", txns)

def load_transactions():
    return load("transactions.json", default=[])

def save_budgets(budgets):
    save("budgets.json", budgets)

def load_budgets():
    return load("budgets.json", default=[])

def save_goals(goals):
    save("goals.json", goals)

def load_goals():
    return load("goals.json", default=[])

def save_notifications(notifs):
    save("notifications.json", notifs)

def load_notifications():
    return load("notifications.json", default=[])