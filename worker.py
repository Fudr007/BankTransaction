import threading
import queue
from accounts import AccountList

class WorkerStopped(Exception):
    pass


class WorkerPool:
    def __init__(self, account_list: AccountList, workers_count=4):
        self.account_list = account_list
        self.tasks = queue.Queue()
        self.workers = []
        self.running = threading.Event()
        self.running.set()

        for i in range(workers_count):
            t = threading.Thread(target=self._worker_loop, name=f"worker-{i}", daemon=True)
            self.workers.append(t)

    def start(self):
        """Spustí všechna vlákna."""
        for t in self.workers:
            t.start()

    def stop(self):
        """Zastaví vlákna korektně."""
        self.running.clear()

        # pošleme None aby se vlákna probudila
        for _ in self.workers:
            self.tasks.put(None)

        for t in self.workers:
            t.join()

    def add_task(self, task):
        """
        Přidá transakci do fronty (producer).
        Může to být Deposit nebo Transaction.
        """
        self.tasks.put(task)

    def _worker_loop(self):
        """
        Worker spotřebovává úkoly.
        Pokud úkol = None → končí.
        """
        while self.running.is_set():
            task = self.tasks.get()
            if task is None:
                break

            try:
                # Executing task
                task.execute()

            except Exception as e:
                print(f"[{threading.current_thread().name}] ERROR: {e}")

            finally:
                self.tasks.task_done()

        # vlákno končí
        return