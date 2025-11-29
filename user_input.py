import sys

from accounts import AccountList, Account
from transactions import DepositTransaction, TransferTransaction


def transfer(accounts):
    yield "Select account to transfer from"
    from_account = yield from select_account(accounts)
    yield "Select account to transfer to"
    to_account = yield from select_account(accounts)

    amount:int|float = yield "Enter transfer amount:"

    t = TransferTransaction(int(amount), from_account, to_account)
    t.execute()
    yield f"Transferred {amount} from account {from_account.get_id()} to account {to_account.get_id()}"
    return

def deposit(accounts):
    yield "Select deposit account"
    account = yield from select_account(accounts)
    amount:int|float = yield "Enter deposit amount:"

    t = DepositTransaction(int(amount), account)
    t.execute()
    yield f"Deposited {amount} to account {account.get_id()}"
    return

def select_account(accounts):
    yield from show_accounts(accounts)
    index = yield "Enter index of the account number:"
    return accounts.get_index(int(index))

def show_accounts(account_list):
    list_print = ""
    i = 1
    for account in account_list:
        list_print += f"{i}. Account with number {account.get_id()} and balance {account.get_balance()}\n"
        i += 1
    yield list_print

def shutdown(accounts):
    accounts.export_json("bank_accounts.json")
    sys.exit()

action_list = {
    0: shutdown,
    1: deposit,
    2: transfer,
    3: show_accounts
}

def menu():
    accounts = AccountList()
    accounts.import_json("bank_accounts.json")
    print("Bank IS")
    print("Actions: 0.Exit, 1. Deposit, 2.Transfer, 3. Show accounts")

    while True:
        try:
            action = int(input("Enter action: "))
            gen = action_list[action](accounts)

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