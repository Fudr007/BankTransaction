import threading
import queue
import time


class TransactionWorkerPool:
    """
    Multithreaded worker pool with producer and consumer.
    """

    def __init__(self, num_workers=2):
        self.queue = queue.Queue()
        self.shutdown_event = threading.Event()
        self.num_workers = num_workers
        self.workers = []

    def start(self):
        """
        Starts all worker threads.
        """
        for i in range(self.num_workers):
            t = threading.Thread(
                target=self.worker_loop,
                args=(i,),
                daemon=True
            )
            self.workers.append(t)
            t.start()


    def stop(self):
        """
        Stops all worker threads and waits for them to finish.
        """
        self.shutdown_event.set()

        for _ in range(self.num_workers):
            self.queue.put(None)

        for t in self.workers:
            t.join()

    def submit(self, transaction):
        """
        Adds a new transaction/task to the queue.
        :param transaction: Task to add to the queue.
        """
        self.queue.put(transaction)

    def worker_loop(self):
        """
        Loop that processes tasks from the queue.
        """
        while not self.shutdown_event.is_set():
            task = self.queue.get()

            if task is None:
                break

            try:
                task.execute()
            except Exception as e:
                raise e

            self.queue.task_done()
