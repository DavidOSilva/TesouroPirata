import threading

class Monitor:
    def __init__(self):
        self.condition = threading.Condition()
        self.inUse = False  # Indica se o recurso está em uso

    def enter(self):
        with self.condition:
            while self.inUse: 
                self.condition.wait() # Espera até que o recurso não esteja mais em uso
            self.inUse = True  # Marca o recurso como em uso

    def leave(self):
        with self.condition:
            self.inUse = False  # Libera o recurso
            self.condition.notify()  # Notifica todas as threads esperando na condição
