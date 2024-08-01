from models.RectWithSprite import *
from consts.Settings import *
import threading

class SharedChest(RectWithSprite):

    def __init__(self, position=stts.sharedChestPosition, size=stts.sharedChestSize):
        self.treasures = []
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.inUse = False
        self.inUseWithoutTreasure = False
        super().__init__(position, size)

    def _setImagePath(self):
        imagePath = "assets/sharedChest/sharedChestClosed.png"
        if self.inUse:
            if self.inUseWithoutTreasure: imagePath = "assets/sharedChest/sharedChestOpenNoTreasure.png"
            else: imagePath = "assets/sharedChest/sharedChestOpen.png"
        return imagePath
    
    def _countTreasures(self):
        playerScores = {}
        for treasure, playerID in self.treasures:
            if playerID not in playerScores: playerScores[playerID] = 0
            playerScores[playerID] += treasure.rarity
        return playerScores
    
    def determineWinner(self):
        scores = self._countTreasures()
        if scores=={}:
            print("Ninguém depositou nenhum tesouro. 🦜🏝️")
            return
        maxScore = max(scores.values())
        winners = [player for player, score in scores.items() if score == maxScore]
        if len(winners) == 1: print(f"O pirata {winners[0]} é o vencedor! 🏆")
        else: print(f"Empate! 🧭")
    

