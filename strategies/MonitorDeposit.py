from interfaces.IDepositStrategy import *
from consts.Settings import *
import time

class MonitorDeposit(IDepositStrategy):
    def deposit(self, Pirate, SharedChest):
        waiting = False
        print(f'O pirata {Pirate.id} tentou acessar o baú da tripulação... 🏴‍☠️')
        if SharedChest.synchMechanism.inUse == True:
            print(f'O pirata {Pirate.id} vai precisar aguardar o baú ser liberado. ⛔')
            start = time.time()
            waiting = True
        SharedChest.synchMechanism.enter()  # Adquire o semáforo.
        if waiting is True: SharedChest.totalWaitTime += time.time() - start  # Acumula tempo.
        try:
            SharedChest.inUse = True
            print(f'O pirata {Pirate.id} conseguiu abrir o baú. ✅')
            if len(Pirate.backpack) > 0: SharedChest.addTreasure(Pirate)
            else:
                SharedChest.inUseWithoutTreasure = True
                time.sleep((stts.depositDuration / 3.5) / 1000)  # Segura um tempinho para animar a abertura do baú.
                if not SharedChest.gameOver.is_set(): print(f'O pirata {Pirate.id} não tem nenhum tesouro, fechando baú... 🪙❓')
        finally:
            SharedChest.synchMechanism.leave()  # Libera o semáforo
            SharedChest.inUse, SharedChest.inUseWithoutTreasure, Pirate.cannotMove = False, False, False  # Libera movimentos e muda sprite do baú.
            if not SharedChest.gameOver.is_set():
                # print(f"O pirata {Pirate.id} viu os seguintes tesouros no baú: {SharedChest.showTreasures()} 💍")
                print(f"O pirata {Pirate.id} liberou o baú. 🔓")