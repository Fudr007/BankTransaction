import threading

from accounts import Account, AccountError, Bank
from transactions import Transaction

def thread_make(transaction):
    if type(transaction) is not Transaction:
        raise TypeError('Must be type of Transaction')

    thread = threading.Thread(target=transaction.execute)
    thread.start()
    thread.join()

if "__main__" == __name__:
    bank = Bank()
    while True:
        pass
