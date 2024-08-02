from abc import ABC, abstractmethod

class IDepositStrategy(ABC):
    
    @abstractmethod
    def deposit(self, Pirate, SharedChest):
        pass
