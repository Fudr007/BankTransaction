import time
from accounts import Account

class TransactionError(Exception):
    pass

class BaseTransaction:
    """
    Base class for all transactions.
    Handles amount, thread-safety, and ID generation.
    """
    def __init__(self, amount):
        self.set_amount(amount)
        self.tx_id = hash((amount, time.time()))

    def set_amount(self, amount):
        #if not isinstance(amount, (int, float)):
        #    raise TransactionError('Amount must be a number')
        #if isinstance(amount, int):
        #    amount = float(amount)
        if float(amount) < 0.0:
            raise ValueError('Amount cannot be negative')
        self.amount = amount

    def execute(self):
        """
        Each subclass must implement this.
        """
        raise NotImplementedError("Subclasses must implement execute()")


class TransferTransaction(BaseTransaction):
    """
    Transfer amount from one account to another.
    """
    def __init__(self, amount, from_account: Account, to_account: Account):
        super().__init__(amount)
        self.set_from_account(from_account)
        self.set_to_account(to_account)
        self.check_accounts()
        # include accounts in tx_id for uniqueness
        self.tx_id = hash((from_account.get_id(), to_account.get_id(), self.amount, time.time()))

    def set_from_account(self, account):
        if not isinstance(account, Account):
            raise TransactionError("from_account must be Account")
        self.from_account = account

    def set_to_account(self, account):
        if not isinstance(account, Account):
            raise TransactionError("to_account must be Account")
        self.to_account = account

    def check_accounts(self):
        if self.from_account.get_id() == self.to_account.get_id():
            raise TransactionError("Cannot transfer to the same account")

    def execute(self):
        # Deadlock prevention by locking accounts in ID order
        acc1, acc2 = sorted([self.from_account, self.to_account], key=lambda x: x.get_id())
        with acc1.lock:
            with acc2.lock:
                if self.from_account.withdraw(self.amount):
                    self.to_account.deposit(self.amount)
        return True

class DepositTransaction(BaseTransaction):
    """
    Deposit an amount into a single account.
    """

    def __init__(self, amount, to_account: Account):
        super().__init__(amount)
        self.set_account(to_account)
        self.tx_id = hash((to_account.get_id(), self.amount, time.time()))

    def set_account(self, account):
        if not isinstance(account, Account):
            raise TransactionError("to_account must be Account")
        self.to_account = account

    def execute(self):
        with self.to_account.lock:
            self.to_account.deposit(self.amount)
            print(f"deposited {self.amount}")
        return True