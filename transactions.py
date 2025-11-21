import time
from command import command

class TransactionError(Exception):
    pass

class Transaction:
    def __init__(self, src, dst, amount):
        self.set_src(src)
        self.set_dst(dst)
        self.set_amount(amount)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S')

    def execute(self):
        raise NotImplementedError()

    def set_src(self, src):
        if (type(src) is not int) or (src < 0):
            raise TransactionError("Source account id must be positive number")
        self.src = src

    def set_dst(self, dst):
        if (dst is not int) or (dst < 0):
            raise TransactionError("Destination account id must be positive number")
        self.dst = dst

    def set_amount(self, amount):
        if (amount is not int) or (amount < 0):
            raise TransactionError("Amount must be positive number")
        self.amount = amount

class DepositTransaction(Transaction):
    def execute(self):
        self.dst.deposit(self.amount)

class WithdrawTransaction(Transaction):
    def execute(self):
        self.dst.withdraw(self.amount)

class TransferTransaction(Transaction):
    def execute(self):
        self.dst.deposit(self.amount)
        self.src.withdraw(self.amount)