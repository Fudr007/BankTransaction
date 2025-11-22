import unittest
from unittest.mock import patch
import threading

from accounts import Account, AccountError
from main import transaction_make
from transactions import Deposit, TransactionError, Transaction

class TestAccount(unittest.TestCase):

    def test_deposit(self):
        acc = Account(1)
        acc.deposit(100)
        self.assertEqual(acc.get_balance(), 100)

    def test_withdraw(self):
        acc = Account(1)
        acc.deposit(200)
        acc.withdraw(100)
        self.assertEqual(acc.get_balance(), 100)

    def test_withdraw_insufficient(self):
        acc = Account(1)
        with self.assertRaises(AccountError):
            acc.withdraw(50)

    def test_negative_deposit(self):
        acc = Account(1)
        with self.assertRaises(AccountError):
            acc.deposit(-5)


class TestDeposit(unittest.TestCase):

    @patch("time.sleep", return_value=None)
    def test_deposit_execution(self, _):
        acc = Account(1)
        dep = Deposit(50, acc)
        dep.execute()
        self.assertEqual(acc.get_balance(), 50)

    def test_deposit_validation(self):
        acc = Account(1)
        with self.assertRaises(ValueError):
            Deposit(-2, acc)
        with self.assertRaises(TransactionError):
            Deposit(10, "not account")


class TestTransaction(unittest.TestCase):

    @patch("time.sleep", return_value=None)
    def test_transaction_execution(self, _):
        acc1 = Account(1)
        acc2 = Account(2)
        acc1.deposit(100)

        tx = Transaction(40, acc1, acc2)
        tx.execute()

        self.assertEqual(acc1.get_balance(), 60)
        self.assertEqual(acc2.get_balance(), 40)

    def test_transaction_negative_amount(self):
        acc1 = Account(1)
        acc2 = Account(2)
        with self.assertRaises(ValueError):
            Transaction(-5, acc1, acc2)

    def test_transaction_same_account(self):
        acc = Account(1)
        with self.assertRaises(TransactionError):
            Transaction(10, acc, acc)

    def test_transaction_account_type(self):
        acc1 = Account(1)
        with self.assertRaises(TransactionError):
            Transaction(10, acc1, "not account")

    @patch("time.sleep", return_value=None)
    def test_transaction_locks_work(self, _):
        acc1 = Account(1)
        acc2 = Account(2)
        acc1.deposit(200)

        tx1 = Transaction(50, acc1, acc2)
        tx2 = Transaction(50, acc1, acc2)

        t1 = threading.Thread(target=tx1.execute)
        t2 = threading.Thread(target=tx2.execute)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(acc1.get_balance(), 100)
        self.assertEqual(acc2.get_balance(), 100)


class TestTransactionMakeGenerator(unittest.TestCase):

    @patch("time.sleep", return_value=None)
    def test_generator_deposit(self, _):
        acc1 = Account(1)
        acc2 = Account(2)

        gen = transaction_make(acc1, acc2)

        self.assertEqual(next(gen), "Deposit (d) / Transfer (t):")
        self.assertEqual(gen.send("d"), "To which account (1/2):")
        self.assertEqual(gen.send("1"), "How much:")
        gen.send("50")   # this triggers the thread

        # allow thread to finish instantly because sleep is patched
        self.assertEqual(acc1.get_balance(), 50)

    @patch("time.sleep", return_value=None)
    def test_generator_transfer(self, _):
        acc1 = Account(1)
        acc2 = Account(2)
        acc1.deposit(100)

        gen = transaction_make(acc1, acc2)

        self.assertEqual(next(gen), "Deposit (d) / Transfer (t):")
        self.assertEqual(gen.send("t"), "To which account (1/2):")
        self.assertEqual(gen.send("2"), "How much:")
        gen.send("30")

        self.assertEqual(acc1.get_balance(), 70)
        self.assertEqual(acc2.get_balance(), 30)

    def test_generator_invalid_type(self):
        acc1 = Account(1)
        acc2 = Account(2)

        gen = transaction_make(acc1, acc2)
        next(gen)
        with self.assertRaises(Exception):
            gen.send("x")

    def test_generator_invalid_account(self):
        acc1 = Account(1)
        acc2 = Account(2)

        gen = transaction_make(acc1, acc2)
        next(gen)
        gen.send("d")
        with self.assertRaises(Exception):
            gen.send("9")

    def test_generator_invalid_money(self):
        acc1 = Account(1)
        acc2 = Account(2)

        gen = transaction_make(acc1, acc2)
        next(gen)           # ask d/t
        gen.send("d")       # ok
        gen.send("1")       # ok
        with self.assertRaises(Exception):
            gen.send("not_number")


if __name__ == "__main__":
    unittest.main()
