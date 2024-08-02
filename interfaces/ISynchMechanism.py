from abc import ABC, abstractmethod

class ISynchMechanism(ABC):

    @abstractmethod
    def acquire(self):
        pass

    @abstractmethod
    def release(self):
        pass