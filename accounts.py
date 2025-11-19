import threading

class Account:
    def __init__(self, id, balance,history):
        self._id = id
        self._balance = balance
        self.lock = threading.Lock
        self.history = history

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def get_balance(self):
        return self._balance