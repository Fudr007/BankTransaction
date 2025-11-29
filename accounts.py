import json
import threading
import time
import uuid


class AccountError(Exception):
    pass

class Account:
    """
    Class representing an account
    """
    def __init__(self, acc_id = 0, balance=0.0):
        self.set_acc_id(acc_id)
        self.set_balance(balance)
        self.lock = threading.Lock()

    def set_acc_id(self, acc_id):
        if type(acc_id) is not int:
            raise AccountError('Account ID must be an integer')

        if acc_id == 0:
            acc_id = uuid.uuid4().int

        self._acc_id = acc_id

    def get_id(self):
        return self._acc_id

    def set_balance(self, amount):
        if type(amount) is not float:
            raise AccountError('Amount must be a float')
        if amount < 0.0:
            raise AccountError('Amount cannot be negative')

        self._balance = amount

    def get_balance(self):
        return self._balance

    def withdraw(self, amount):
        """
        Withdraws the amount of money from the account
        :param amount: amount to withdraw
        :return: True if everything is fine
        """
        if type(amount) is not int:
            raise AccountError('Amount must be a number')
        if amount > self._balance:
            raise AccountError('Cant withdraw more than your is on your account')

        self._balance -= amount

        return True

    def deposit(self, amount):
        """
        Deposits the amount of money from the account
        :param amount: amount to deposit
        :return: True if everything is fine
        """
        if type(amount) is not int:
            raise AccountError('Amount must be a number')

        if amount < 0:
            raise AccountError('Amount cannot be negative')

        self._balance += amount
        return True

    def to_dict(self):
        return {
            "acc_id": self._acc_id,
            "balance": self._balance
        }

    @staticmethod
    def from_dict(data):
        return Account(acc_id=data["acc_id"], balance=float(data["balance"]))


class AccountList():
    def __init__(self):
        self.accounts = {}

    def add_account(self, acc):
        self.accounts[acc.get_id()] = acc

    def get_index(self, index):
        now_i = 1
        for account in self.accounts.values():
            if now_i == index:
                return account
            now_i += 1

        raise AccountError('Account with such index does not exist')

    def __iter__(self):
        return iter(self.accounts.values())

    def to_dict(self):
        return {
            "accounts": {
                str(acc_id): acc.to_dict()
                for acc_id, acc in self.accounts.items()
            }
        }

    @staticmethod
    def from_dict(data):
        acc_list = AccountList()
        for acc_id, acc_data in data["accounts"].items():
            a = Account.from_dict(acc_data)
            acc_list.add_account(a)
        return acc_list

    def export_json(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def import_json(self, path):
        with open(path, "r") as file:
            data = json.load(file)
        restored = AccountList.from_dict(data)
        self.accounts = restored.accounts