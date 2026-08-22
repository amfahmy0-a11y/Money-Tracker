import json
import os
from models import Expense

EXPENSES_FILE = "expenses_data.json"
SETTINGS_FILE = "user_settings.json"

def save_all_data(expenses_list, settings_obj):
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in expenses_list], f, ensure_ascii=False, indent=4)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings_obj.to_dict(), f, ensure_ascii=False, indent=4)

def load_all_data():
    expenses = []
    settings_data = {"username": "المستخدم", "language": "ar", "dark_mode": True}
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                expenses = [Expense(item["name"], item["amount"], item["date"]) for item in data]
            except Exception:
                expenses = []
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            try:
                settings_data = json.load(f)
            except Exception:
                pass
    return expenses, settings_data
