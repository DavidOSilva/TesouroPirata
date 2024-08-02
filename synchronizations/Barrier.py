import threading

class Barrier():
    def __init__(self, count=2):
        self._count = count
        self._current_count = 0
        self._condition = threading.Condition()

    def wait(self): # Aguarda até que todas as threads alcancem a barreira.
        with self._condition:
            self._current_count += 1
            if self._current_count < self._count:  self._condition.wait() # Se nem todas as threads chegaram, espera.
            else: # Se todas as threads chegaram, reinicia o contador e notifica todas.
                self._current_count = 0
                self._condition.notify_all()