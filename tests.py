import unittest
from unittest.mock import Mock
import threading

from accounts import Account, AccountError
from transactions import DepositTransaction, TransferTransaction, TransactionError

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


class TestDepositTransaction(unittest.TestCase):

    def test_deposit_execution(self):
        acc = Account(1)
        dep = DepositTransaction(50, acc)
        dep.execute()
        self.assertEqual(acc.get_balance(), 50)

    def test_deposit_validation(self):
        acc = Account(1)
        with self.assertRaises(ValueError):
            DepositTransaction(-2, acc)
        with self.assertRaises(TransactionError):
            DepositTransaction(10, "not account")


class TestTransferTransaction(unittest.TestCase):

    def test_transaction_execution(self):
        acc1 = Account(1)
        acc2 = Account(2)
        acc1.set_balance(100.0)

        tx = TransferTransaction(40, acc1, acc2)
        tx.execute()

        self.assertEqual(acc1.get_balance(), 60)
        self.assertEqual(acc2.get_balance(), 40)

    def test_transaction_negative_amount(self):
        acc1 = Account(1)
        acc2 = Account(2)
        with self.assertRaises(ValueError):
            TransferTransaction(-5, acc1, acc2)

    def test_transaction_same_account(self):
        acc = Account(1)
        with self.assertRaises(TransactionError):
            TransferTransaction(10, acc, acc)

    def test_transaction_account_type(self):
        acc1 = Account(1)
        with self.assertRaises(TransactionError):
            TransferTransaction(10, acc1, "not account")

    def test_transaction_locks_work(self):
        acc1 = Account(1)
        acc2 = Account(2)
        acc1.set_balance(200.0)

        tx1 = TransferTransaction(50, acc1, acc2)
        tx2 = TransferTransaction(50, acc1, acc2)

        t1 = threading.Thread(target=tx1.execute)
        t2 = threading.Thread(target=tx2.execute)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(acc1.get_balance(), 100)
        self.assertEqual(acc2.get_balance(), 100)


class TestUserInputGenerators(unittest.TestCase):

    def test_deposit_generator_submits_to_pool(self):
        from user_input import deposit
        # Prepare accounts and fake pool
        acc1 = Account(1)
        pool = Mock()

        gen = deposit(_FakeAccountList([acc1]), pool)

        # First yield asks to select deposit account
        msg = next(gen)
        self.assertIn("Select deposit account", msg)
        # Then shows accounts list
        msg = next(gen)
        self.assertIn("Account with number", msg)
        # Prompt for index
        msg = next(gen)
        self.assertIn("Enter index", msg)
        # Send index 1 -> then asks amount
        msg = gen.send("1")
        self.assertIn("Enter deposit amount", msg)
        # Send amount; should submit a DepositTransaction
        done = gen.send("50")
        self.assertIn("Deposit transaction", done)

        self.assertTrue(pool.submit.called)
        submitted = pool.submit.call_args.args[0]
        self.assertIsInstance(submitted, DepositTransaction)
        self.assertEqual(submitted.amount, 50)

    def test_transfer_generator_submits_to_pool(self):
        from user_input import transfer
        acc1 = Account(1)
        acc2 = Account(2)
        pool = Mock()

        gen = transfer(_FakeAccountList([acc1, acc2]), pool)

        # From account
        self.assertIn("Select account to transfer from", next(gen))
        self.assertIn("Account with number", next(gen))
        self.assertIn("Enter index", next(gen))
        # choose from acc1
        self.assertIn("Select account to transfer to", gen.send("1"))
        # show accounts again
        self.assertIn("Account with number", next(gen))
        self.assertIn("Enter index", next(gen))
        # choose to acc2 -> ask amount
        self.assertIn("Enter transfer amount", gen.send("2"))
        # enter amount
        done = gen.send("30")
        self.assertIn("Transfer transaction", done)

        self.assertTrue(pool.submit.called)
        submitted = pool.submit.call_args.args[0]
        self.assertIsInstance(submitted, TransferTransaction)
        self.assertEqual(submitted.amount, 30)


class _FakeAccountList:
    """Minimal adapter to satisfy user_input helpers."""
    def __init__(self, accounts):
        self._accounts = accounts

    def __iter__(self):
        return iter(self._accounts)

    def get_index(self, index):
        return self._accounts[index - 1]


if __name__ == "__main__":
    unittest.main()
