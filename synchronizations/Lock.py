import threading

class Lock:
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self, timeout=0.5):
        return self.lock.acquire(timeout=timeout) # O timeout é o tempo máximo em segundos para tentar adquirir o lock.

    def release(self):
        self.lock.release() # Libera o lock adquirido.