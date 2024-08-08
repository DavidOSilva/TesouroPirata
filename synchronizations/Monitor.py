import threading

class Monitor:
    def __init__(self):
        self.lock = threading.Lock() # Inicializa um lock e uma condição com o lock
        self.condition = threading.Condition(self.lock)
        self.inUse = False  # Indica se o recurso está em uso

    def enter(self):
        with self.lock: # Adquire o lock antes de acessar a seção crítica
            while self.inUse: # Espera até que o recurso não esteja mais em uso
                self.condition.wait()
            self.inUse = True  # Marca o recurso como em uso

    def leave(self):
        with self.lock:
            self.inUse = False  # Libera o recurso
            self.condition.notify_all()  # Notifica todas as threads esperando na condição
