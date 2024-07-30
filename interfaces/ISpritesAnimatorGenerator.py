from abc import ABC, abstractmethod

class ISpritesAnimatorGenerator(ABC):

    @abstractmethod
    def _loadSpritesFromJson(self, pngSprites, jsonSheet): # Método abstrato para desenhar o objeto na tela.
        pass