from consts.Settings import *
from models.RectWithSprite import *
from pathlib import Path

class Treasure(RectWithSprite):

    def __init__(self, position, rarity, size=stts.treasureSize):
        self.rarity = rarity
        self.imagePath = self._setImagePath()  # Defina self.imagePath baseado em rarity
        super().__init__(position=position, size=size)

    def _setImagePath(self):
        if self.rarity  == min(stts.treasureValues): imagePath = Path("assets/treasure/treasureBronze.png")
        elif self.rarity  == stts.treasureValues[1]: imagePath = Path("assets/treasure/treasureSilver.png")
        else: imagePath = Path("assets/treasure/treasureGold.png")
        return imagePath
    
    def identifyRarity(self):
        if self.rarity == max(stts.treasureValues): return "Ouro. 🥇"
        elif self.rarity == stts.treasureValues[1]: return "Prata. 🥈"
        elif self.rarity == min(stts.treasureValues): return "Bronze. 🥉"
        else: return "Outro"
