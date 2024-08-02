from consts.Settings import *
from interfaces.IDepositStrategy import *
from interfaces.ISynchMechanism import *
from strategies.synchronizations.Semaphore import *
from strategies.synchronizations.Lock import *
from strategies.deposits.LockDeposit import *
from strategies.deposits.SemaphoreDeposit import *

class SynchMechanismFactory:

    def __init__(self, mechanism=stts.synchMenchanism.lower()):
        self.mechanism = mechanism

    def createSynchMechanism(self) -> ISynchMechanism:
        if self.mechanism == "semaphore":  return Semaphore()
        elif self.mechanism == "lock": return Lock()
        else: raise ValueError(f"Mecanismo de sincronização de processos inválido: {self.mechanism}")

    def createDeposityStrategy(self) ->  IDepositStrategy:
        if self.mechanism == "semaphore":  return SemaphoreDeposit()
        elif self.mechanism == "lock": return LockDeposit()
        else: raise ValueError(f"Mecanismo de sincronização de processos inválido: {self.mechanism}")
