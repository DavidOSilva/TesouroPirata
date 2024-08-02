from interfaces.IDepositStrategy import *
from consts.Settings import *
import time

class SemaphoreDeposit(IDepositStrategy):
    def deposit(self, Pirate, SharedChest):
        print(f'O pirata {Pirate.id} tentou acessar o baú da tripulação... 🏴‍☠️')
        if SharedChest.synchMechanism.value == 0: print(f'O pirata {Pirate.id} vai precisar aguardar o baú ser liberado. ⛔')
        SharedChest.synchMechanism.acquire()  # Adquire o semáforo
        try:
            SharedChest.inUse = True
            print(f'O pirata {Pirate.id} conseguiu abrir o baú. ✅')
            if len(Pirate.backpack) > 0: SharedChest.addTreasure(Pirate)
            else:
                SharedChest.inUseWithoutTreasure = True
                time.sleep((stts.depositDuration / 3.5) / 1000)  # Segura um tempinho para animar a abertura do baú.
                if not SharedChest.gameOver.is_set(): print(f'O pirata {Pirate.id} não tem nenhum tesouro, fechando baú... 🪙❓')
        finally:
            SharedChest.synchMechanism.release()  # Libera o semáforo
            SharedChest.inUse, SharedChest.inUseWithoutTreasure, Pirate.cannotMove = False, False, False  # Libera movimentos e muda sprite do baú.
            if not SharedChest.gameOver.is_set():
                print(f"O pirata {Pirate.id} liberou o baú. 🔓")
                #print(f"Tesouros depositados no baú: {SharedChest.showTreasures()} 💍")