from consts.Colors import *
import pygame

class RectText():

    def __init__(self, text, position, sizeFont=36, color=colors.black):
        self.text = text
        self.position = position
        self.color = color
        self.sizeFont = sizeFont
        self.font = pygame.font.Font(None, self.sizeFont)
        self.surface = self._renderSurface()

    def _renderSurface(self): return self.font.render(self.text, True, self.color)

    def _draw(self, win): win.blit(self.surface, self.position)