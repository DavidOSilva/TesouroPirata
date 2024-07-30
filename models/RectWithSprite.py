import pygame

class RectWithSprite:
    def __init__(self, position, size, image=None, sprite=None):
        self.position = position
        self.size = size
        self.imagePath = image if image is not None else self._setImagePath()
        self.sprite = sprite if sprite is not None else self._setSprite()
    
    def getRect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def _setImagePath(self):
        pass

    def _setSprite(self):
        sprite = pygame.image.load(self.imagePath).convert_alpha()
        sprite = pygame.transform.scale(sprite, (self.size[0],self.size[1])).convert_alpha()
        return sprite
    
    def _update(self):
        self.imagePath = self._setImagePath()
        self.sprite = self._setSprite()
    
    def _draw(self, win):
        self._update()
        win.blit(self.sprite, self.position)