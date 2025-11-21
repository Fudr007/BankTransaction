import threading
from command import command

class AccountError(Exception):
    pass

class Account:
    def __init__(self, acc_id):
        self.set_acc_id(acc_id)
        self._balance = 0
        self._lock = threading.Lock()

    def set_acc_id(self, acc_id):
        if type(acc_id) is not int:
            raise AccountError("Account ID must be an integer")
        if acc_id < 0:
            raise AccountError("Account ID must be positive number")

        self._acc_id = acc_id

    def get_id(self):
        return self._acc_id

    @command("Withdraw")
    def withdraw(self, amount):
        if type(amount) is not int:
            raise AccountError('Amount must be a number')
        with self._lock:
            if amount > self._balance:
                raise AccountError('Cant withdraw more than your is on your account')
            self._balance -= amount

    @command("Deposit")
    def deposit(self, amount):
        if type(amount) is not int:
            raise AccountError('Amount must be a number')
        with self._lock:
            self._balance += amount

    @command("Get balance")
    def get_balance(self):
        return self._balance

class BankError(Exception):
    pass

class Bank:
    def __init__(self):
        self.accounts = {}

    @command("Make account")
    def add_new_account(self, acc_id):
        if type(acc_id) is not int:
            raise AccountError("Account ID must be an integer")
        if acc_id in self.accounts:
            raise BankError("Account with this id already exists")

        acc = Account(acc_id)
        self.accounts[acc.get_id()] = acc

    @command("Delete account")
    def del_account(self, acc_id):
        if acc_id in self.accounts:
            del self.accounts[acc_id]
        else:
            raise AccountError('Account with this id was not found in this bank')