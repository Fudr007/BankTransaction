import sys

from accounts import AccountList, Account
from transactions import DepositTransaction, TransferTransaction
from worker import TransactionWorkerPool


def transfer(account_list, pool):
    """
    Is generator function, which makes Transfer transaction with user input
    :param account_list: List of accounts
    :param pool: Pool of workers
    :return: Nothing
    """
    yield "Select account to transfer from"
    from_account = yield from select_account(account_list)
    yield "Select account to transfer to"
    to_account = yield from select_account(account_list)

    amount:int|float = yield "Enter transfer amount:"

    t = TransferTransaction(int(amount), from_account, to_account)
    pool.submit(t)
    yield f"Transferred {amount} from account {from_account.get_id()} to account {to_account.get_id()}"
    return

def deposit(account_list, pool):
    """
    Is generator function, which makes Deposit transaction with user input
    :param account_list: List of accounts
    :param pool: Pool of workers
    :return: Nothing
    """
    yield "Select deposit account"
    account = yield from select_account(account_list)
    amount:int|float = yield "Enter deposit amount:"

    t = DepositTransaction(int(amount), account)
    pool.submit(t)
    yield f"Deposited {amount} to account {account.get_id()}"
    return

def select_account(account_list):
    """
    Is generator function, which shows accounts and asks user to select one
    :param account_list: List of accounts
    :return: selected account
    """
    yield from show_accounts(account_list)
    index = yield "Enter index of the account number:"
    return account_list.get_index(int(index))

def show_accounts(account_list):
    """
    Yields list of accounts
    :param account_list: List of accounts
    :return: List of accounts in string format
    """
    list_print = ""
    i = 1
    for account in account_list:
        list_print += f"{i}. Account with number {account.get_id()} and balance {account.get_balance()}\n"
        i += 1
    yield list_print

def make_acc(account_list):
    """
    Creates new account and adds it to list of accounts
    :param account_list: List of accounts
    :return: Information that the action was performed
    """
    acc = Account()
    account_list.add_account(acc)
    yield f"Added account {acc.get_id()} to list of accounts"

def shutdown(account_list, pool):
    """
    Shuts down workers and saves accounts to json file
    :param account_list: List of accounts
    :param pool: Pool of workers
    """
    pool.stop()
    account_list.export_json("bank_accounts.json")
    sys.exit()

action_list = {
    0: lambda acc_list, pool: shutdown(acc_list, pool),
    1: lambda acc_list, pool: deposit(acc_list, pool),
    2: lambda acc_list, pool: transfer(acc_list, pool),
    3: lambda acc_list, pool: make_acc(acc_list),
    4: lambda acc_list, pool: show_accounts(acc_list)
}

def menu():
    """
    Main menu of the program, it controls the whole program flow
    """
    pool = TransactionWorkerPool(num_workers=8)
    pool.start()
    accounts = AccountList()
    accounts.import_json("bank_accounts.json")
    print("Bank IS")

    while True:
        print("Actions: 0.Exit, 1. Deposit, 2.Transfer, 3. Create new account, 4. Show accounts")
        try:
            action = int(input("Enter action: "))
            gen = action_list[action](accounts, pool)

            item = next(gen)
            while True:
                print(item)

                if type(item) is str and item.endswith(":"):
                    user_input = input()
                    try:
                        item = gen.send(user_input)
                    except StopIteration:
                        break

                else:
                    try:
                        item = next(gen)
                    except StopIteration:
                        break

        except StopIteration:
            continue
        except ValueError:
            print("Invalid type of input!")
        except Exception as e:
            print("Error:", e)