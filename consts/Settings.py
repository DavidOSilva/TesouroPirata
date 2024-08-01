from consts.Colors import *

class Settings:

    def __init__(self):
        self.width = 1000
        self.height = int(self.width*0.5575)
        self.gameDuration = 60 * 1000
        self.margin = 20

        self.playerSpeed = 7
        self.playerSize = [52, 75]
        self.playerBackpackCapacity = 3
        self.playerAnimationFrameRate = 10

        self.treasureSize = [30, 34]
        self.treasureValues = [1, 3, 5]
        self.treasureProbas = [0.5, 0.35, 0.15]
        self.treasureNumMax = 15
        self.treasureSpawnInterval = 4 * 1000 
        self.treasureSpawnAmount = 2

        self.sharedChestSize = [54, 54]
        self.sharedChestPosition = self.width // 2 - self.sharedChestSize[0] // 2, self.height // 2 - self.sharedChestSize[1] // 2
        self.depositDuration = 1.2 * 1000

stts = Settings()