import threading

from accounts import Account, AccountError
from transactions import Transaction, TransactionError, Deposit, transaction_make

'''
if "__main__" == __name__:
    account1 = Account(1)
    account2 = Account(2)
    try:
        deposit = Deposit(10000, account1)
        thread = threading.Thread(target=deposit.execute)
        deposit1 = Deposit(10000, account2)
        thread1 = threading.Thread(target=deposit1.execute)
        transaction = Transaction(100, account1, account2)
        thread2 = threading.Thread(target=transaction.execute)
        transaction1 = Transaction(500, account1, account2)
        thread3 = threading.Thread(target=transaction1.execute)
        transaction2 = Transaction(5000, account2, account1)
        thread4 = threading.Thread(target=transaction2.execute)
        transaction3 = Transaction(1000, account1, account2)
        thread5 = threading.Thread(target=transaction3.execute)
        transaction4 = Transaction(20, account2, account1)
        thread6 = threading.Thread(target=transaction4.execute)
        pool.append(thread)
        pool.append(thread1)
        pool.append(thread2)
        pool.append(thread3)
        pool.append(thread4)
        pool.append(thread5)
        pool.append(thread6)
    except Exception as e:
        print(e)

    try:
        start_transactions()
    except Exception as e:
        print(e)
    
    #acc1 = 10000 - 100 - 500 + 5000 - 1000 + 20 = 13420
    #acc2= 10000 + 100 + 500 - 5000 + 1000 - 20 = 6580
'''
pool = []

if __name__ == "__main__":
    account1 = Account(1)
    account2 = Account(2)

    while True:
        try:
            print("Account 1 balance:", account1.get_balance())
            print("Account 2 balance:", account2.get_balance())

            reply = input("Do you want to make new transactions? (y/n):")
            if reply == "n":
                for threads in pool:
                    threads.join()
                break
            if reply != "y":
                raise TransactionError("Invalid input")

            gen = transaction_make(account1, account2)

            print(next(gen))
            print(gen.send(input()))
            print(gen.send(input()))
            thread_to_pool=gen.send(input())
            pool.append(thread_to_pool)

        except Exception as e:
            print(e)

    print("Final balance Account 1:", account1.get_balance())
    print("Final balance Account 2:", account2.get_balance())