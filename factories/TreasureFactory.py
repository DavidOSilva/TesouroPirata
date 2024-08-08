from models.Treasure import *
from consts.Settings import *
import random

class TreasureFactory():

    def __init__(self, exclusionZones=[]):
        self.exclusionZones = exclusionZones

    def createTreasures(self, numTreasures=stts.treasureNumMax, probas=stts.treasureProbas, values=stts.treasureValues, isTest=stts.isTest):
        treasureList = []
        if isTest: random.seed(stts.seed) # Fixar a seed para testes, assim todo jogo será o mesmo.
        for _ in range(numTreasures):
            x, y = self._getRandomPosition()
            while any(self._isOverlapping(x, y, zone) for zone in self.exclusionZones): x, y = self._getRandomPosition()
            rarity = random.choices(values, weights=probas)[0]  # Exemplo de escolha de raridade
            treasure = Treasure(position=[x, y], rarity=rarity)
            self.exclusionZones.append(treasure.getRect())
            treasureList.append(treasure)
        return treasureList
        
    @staticmethod
    def _getRandomPosition():
        x = random.randint(stts.margin, stts.width - stts.treasureSize[0] - stts.margin)
        y = random.randint(stts.margin, stts.height - stts.treasureSize[1] - stts.margin)
        return x, y
    
    @staticmethod
    def _isOverlapping(x, y, zone, treasureSize=stts.treasureSize):
        treasureRect = pygame.Rect(x, y, treasureSize[0], treasureSize[1])
        return treasureRect.colliderect(zone)