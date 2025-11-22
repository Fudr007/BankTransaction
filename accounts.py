import threading

class AccountError(Exception):
    pass

class Account:
    """
    Class representing an account
    """
    def __init__(self, acc_id):
        self._acc_id = acc_id
        self._balance = 0
        self.lock = threading.Lock()

    def set_acc_id(self, acc_id):
        if type(acc_id) is not int:
            raise AccountError('Account ID must be an integer')
        if acc_id<0:
            raise AccountError('Account ID cannot be negative')
        self._acc_id = acc_id

    def get_id(self):
        return self._acc_id

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

    def get_balance(self):
        return self._balance