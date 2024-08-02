from interfaces.ISynchMechanism import *
import threading

class Semaphore(ISynchMechanism):
    def __init__(self, value = 1):
        self.value = value # Determina o número máximo de threads que podem acessar a seção crítica simultaneamente.
        self.condition = threading.Condition()
    
    def acquire(self):
        with self.condition: # Método para uma thread esperar para entrar na seção crítica.
            while self.value <= 0: self.condition.wait() # Se o valor for 0 ou menor, a thread espera.
            self.value -= 1 # Decrementa o valor e permite que a thread prossiga.
    
    def release(self):
        with self.condition:  # Método para uma thread sinalizar que está saindo da seção crítica
            self.value += 1  # Incrementa o valor e notifica uma das threads que estão esperando
            self.condition.notify()