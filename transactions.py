import threading
import time

from accounts import Account, AccountError


class TransactionError(Exception):
    pass

class Transaction:
    """
    Class representing a transaction from account to another account
    """
    def __init__(self, amount, from_account, to_account):
        self.set_amount(amount)
        self.set_from_account(from_account)
        self.set_to_account(to_account)
        self.check_acc()
        self.tx_id = hash((from_account.get_id(), to_account.get_id(), amount, time.time()))

    def set_amount(self, amount):
        if type(amount) is not int:
            raise TypeError('Amount must be of type int')
        if amount < 0:
            raise ValueError('Amount cannot be negative')

        self.amount = amount

    def set_to_account(self, account):
        if type(account) is not Account:
            raise TransactionError('Account must be of type Account')

        self.to_account = account

    def set_from_account(self, account):
        if type(account) is not Account:
            raise TransactionError('Account must be of type Account')
        self.from_account = account

    def check_acc(self):
        if self.from_account.get_id() == self.to_account.get_id():
            raise TransactionError('Cannot execute transaction to the same account')

    def execute(self):
        """
        Thread safe executes the transaction
        :return: True if everything is fine
        """
        acc1, acc2 = sorted([self.from_account, self.to_account], key=lambda x: x.get_id()) #deadlock
        with acc1.lock:
            with acc2.lock:
                if self.from_account.withdraw(self.amount):
                    self.to_account.deposit(self.amount)

        return True

class Deposit:
    """
    Class representing a deposit transaction to account
    """
    def __init__(self, amount, to_account):
        self.set_amount(amount)
        self.set_account(to_account)

    def set_amount(self, amount):
        if type(amount) is not int:
            raise TypeError('Amount must be of type int')
        if amount < 0:
            raise ValueError('Amount cannot be negative')
        self.amount = amount

    def set_account(self, account):
        if type(account) is not Account:
            raise TransactionError('Account must be of type Account')
        self.to_account = account

    def execute(self):
        """
        Thread safe executes the deposit transaction
        :return: True if everything is fine
        """
        with self.to_account.lock:
            self.to_account.deposit(self.amount)
        return True