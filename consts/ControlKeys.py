import pygame
from consts.Settings import *

class ControlKeys:

    def __init__(self, playerId):
        self.control = self._createControlKeys(playerId)
        self.left = self.control['left']
        self.right = self.control['right']
        self.up = self.control['up']
        self.down = self.control['down']
        self.action = self.control['action']

    @staticmethod
    def _createControlKeys(playerId, testMode=stts.isTest):
        control = {} 
        if playerId==1:
            control = {
                'left': pygame.K_a,
                'right': pygame.K_d,
                'up': pygame.K_w,
                'down': pygame.K_s,
                'action': pygame.K_f,
        }
        elif playerId == 2:
            control = {
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'up': pygame.K_UP,
                'down': pygame.K_DOWN,
                'action': pygame.K_KP0,
        }
        if testMode: control['action'] = pygame.K_SPACE
        return control