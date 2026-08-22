from datetime import datetime

class Expense:
    def __init__(self, name: str, amount: float, date_str: str):
        self.name = name
        self.amount = amount
        self.date = datetime.strptime(date_str, "%Y-%m-%d").date()

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "date": self.date.strftime("%Y-%m-%d")
        }

class UserSettings:
    def __init__(self, username="المستخدم", language="ar", dark_mode=True):
        self.username = username
        self.language = language
        self.dark_mode = dark_mode

    def to_dict(self):
        return {
            "username": self.username,
            "language": self.language,
            "dark_mode": self.dark_mode
        }
