from interfaces.IDepositStrategy import *
from consts.Settings import *
import time

class LockDeposit(IDepositStrategy):
    def deposit(self, Pirate, SharedChest):
        print(f'O pirata {Pirate.id} tentou acessar o baú da tripulação... 🏴‍☠️')
        acquired = SharedChest.synchMechanism.acquire()
        if acquired:
            try:
                SharedChest.inUse = True
                print(f'O pirata {Pirate.id} conseguiu abrir o baú. ✅')
                if len(Pirate.backpack) > 0: SharedChest.addTreasure(Pirate)
                else:
                    SharedChest.inUseWithoutTreasure = True
                    time.sleep((stts.depositDuration / 3.5) / 1000)  # Segura um tempinho para animar a abertura do baú
                    if not SharedChest.gameOver.is_set(): print(f'O pirata {Pirate.id} não tem nenhum tesouro, fechando baú... 🪙❓')
                    return
            finally:
                SharedChest.synchMechanism.release()
                SharedChest.inUse, SharedChest.inUseWithoutTreasure, Pirate.cannotMove = False, False, False
                if not SharedChest.gameOver.is_set():
                    print(f"O pirata {Pirate.id} viu os seguintes tesouros no baú: {SharedChest.showTreasures()} 💍")
                    print(f"O pirata {Pirate.id} liberou o baú. 🔓")
        else:
            Pirate.cannotMove = False
            if not SharedChest.gameOver.is_set():
                print(f'O pirata {Pirate.id} não conseguiu abrir o baú e precisou aguardar. ⛔')