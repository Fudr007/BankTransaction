import threading
import time
from subprocess import check_call

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
        acc1, acc2 = sorted([self.from_account, self.to_account], key=lambda x: x.get_id())
        time.sleep(10)
        with acc1.lock:
            with acc2.lock:
                if self.from_account.withdraw(self.amount):
                    #print("Withdrawn from account"+str(self.from_account.get_id()))
                    #print(str(self.from_account.get_id())+" "+str(self.from_account.get_balance()))
                    time.sleep(10)
                    self.to_account.deposit(self.amount)
                    #print("Deposit to account" + str(self.from_account.get_id()))
                    #print(str(self.to_account.get_id()) + " " + str(self.to_account.get_balance())

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
        time.sleep(10)
        with self.to_account.lock:
            self.to_account.deposit(self.amount)
        #print("Deposit successful"+str(self.to_account.get_balance()))
        return True


def transaction_make(account1, account2=None):
    """
    Makes a transaction in new thread with user input and starts the thread/transaction
    :param account1: account 1
    :param account2: account 2
    """
    try:
        what = yield "Deposit (d) / Transfer (t):"
        if what not in ("d", "t"):
            raise TransactionError("Invalid transaction type")

        where = yield "To which account (1/2):"
        if where not in ("1", "2"):
            raise TransactionError("Invalid account")

        money = yield "How much:"
        try:
            money = int(money)
        except ValueError:
            raise TransactionError("Amount must be an integer")
        if money < 0:
            raise AccountError("Amount cannot be negative")

        target = account1 if where == "1" else account2

        if what == "d":
            op = Deposit(money, target)
        else:
            if where == "1":
                op = Transaction(money, account2, account1)
            else:
                op = Transaction(money, account1, account2)

        thread = threading.Thread(target=op.execute)

    except Exception as e:
        print(e)

    thread.start()
    yield thread