import time

class Transaction:
    def __init__(self, tx_id, type, src_acc, dst_acc, amount):
        self.tx_id = tx_id
        self.type = type
        self.src_acc = src_acc
        self.dst_acc = dst_acc
        self.amount = amount
        self.timestamp = time.time()