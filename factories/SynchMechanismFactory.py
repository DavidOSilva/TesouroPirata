from consts.Settings import *
from interfaces.IDepositStrategy import *
from interfaces.ISynchMechanism import *
from synchronizations.Semaphore import *
from synchronizations.Lock import *
from synchronizations.Monitor import *
from strategies.LockDeposit import *
from strategies.SemaphoreDeposit import *
from strategies.MonitorDeposit import *

class SynchMechanismFactory:

    def __init__(self, mechanism=stts.synchMenchanism.lower()):
        self.mechanism = mechanism

    def createSynchMechanism(self):
        if self.mechanism == "semaphore":  return Semaphore()
        elif self.mechanism == "lock": return Lock()
        elif self.mechanism == "monitor": return Monitor()
        else: raise ValueError(f"Mecanismo de sincronização de processos inválido: {self.mechanism}")

    def createDeposityStrategy(self) ->  IDepositStrategy:
        if self.mechanism == "semaphore":  return SemaphoreDeposit()
        elif self.mechanism == "lock": return LockDeposit()
        elif self.mechanism == "monitor": return MonitorDeposit()
        else: raise ValueError(f"Mecanismo de sincronização de processos inválido: {self.mechanism}")
