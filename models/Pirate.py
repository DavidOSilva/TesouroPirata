from interfaces.ISpritesAnimatorGenerator import *
from factories.SynchMechanismFactory import *
from models.RectWithSprite import *
from models.SharedChest import *
from models.Treasure import *
from consts.Settings import *
from consts.ControlKeys import *
import time
import threading
import json
from pathlib import Path

class Pirate(ISpritesAnimatorGenerator):

    def __init__(self, id, position, pngSprites, jsonSheet=Path("assets/pirate/pirateSpritesSheet.json"), size=stts.playerSize, state='idle', frame=0):
        self.id = id
        self.backpack = []
        self.control = ControlKeys(self.id)
        self.cannotMove = False
        self.position = position
        self.size = size
        self.state = state
        self.frame = frame
        self.lastUpdate = pygame.time.get_ticks()
        self.spritesToAnimation = self._loadSpritesFromJson(Path(pngSprites), Path(jsonSheet))
        self.sprite = self.spritesToAnimation['idle'][0]
        self.depositStrategy = SynchMechanismFactory().createDeposityStrategy()

    def getRect(self): return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def _draw(self, win): win.blit(self.sprite, self.position)

    def _loadSpritesFromJson(self, pngSprites, jsonSheet): #Metodo herdado de ISpritesGenerator
        with open(jsonSheet) as f: sprite_data = json.load(f)
        sprites, sheet = {}, pygame.image.load(pngSprites).convert_alpha()
        for state, frames in sprite_data.items():
            sprites[state] = []
            for frame in frames.values():
                rect = pygame.Rect(frame['x'], frame['y'], frame['w'], frame['h'])
                sprite = sheet.subsurface(rect)
                sprite = pygame.transform.scale(sprite, self.size)
                sprites[state].append(sprite)
        return sprites
    
    def move(self, keys):
        isLeft = False
        previousState = self.state
        if not self.cannotMove:
            # Atualiza a posição e o estado com base nas teclas pressionadas
            if keys[self.control.left]:
                self.position[0] -= stts.playerSpeed
                self.state = 'walkSide'
                isLeft = True
            elif keys[self.control.right]:
                self.position[0] += stts.playerSpeed
                self.state = 'walkSide'
            elif keys[self.control.up]:
                self.position[1] -= stts.playerSpeed
                self.state = 'walkBack'
            elif keys[self.control.down]:
                self.position[1] += stts.playerSpeed
                self.state = 'walkFoward'
            else: self.state = 'idle'
        else: self.state = 'idle'

        # Atualiza a animação apenas se o estado mudou
        if self.state != previousState: self.frame = 0  # Reseta o frame quando o estado muda

        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 1000 // stts.playerAnimationFrameRate:
            if self.spritesToAnimation[self.state] and self.state != 'idle':  # Garante que o estado tem sprites
                self.frame = (self.frame + 1) % len(self.spritesToAnimation[self.state])
            self.lastUpdate = now

        # Seleciona o sprite correto e aplica o flip se necessário.
        sprite = self.spritesToAnimation[self.state][self.frame] if self.spritesToAnimation[self.state] else pygame.Surface((stts.playerSize[0], stts.playerSize[1]))
        if isLeft: sprite = pygame.transform.flip(sprite, True, False)
        self.sprite = sprite

    def collect(self, treasures, capacity=stts.playerBackpackCapacity):
        treasureCollected = []
        for treasure in treasures:
            treasureRect = treasure.getRect()
            if self.getRect().colliderect(treasureRect) and len(self.backpack) < capacity:
                self.backpack.append(treasure)
                treasureCollected.append(treasure)
                treasures.remove(treasure)
        return treasureCollected

    def _depositTreasure(self, SharedChest): self.depositStrategy.deposit(self, SharedChest)

    def action(self, SharedChest, keyState):
        playerRect, chestRect = self.getRect(), SharedChest.getRect()
        if playerRect.colliderect(chestRect):
            if keyState[self.control.action] and not self.cannotMove:
                self.cannotMove = True
                threading.Thread(target=self._depositTreasure, args=(SharedChest, )).start()

             