from consts.Settings import *
from models.RectText import *

class Chronometer(RectText):

    def __init__(self, timeRemaining, text, position):
        self.timeRemaining = self._formatTime(timeRemaining)
        super().__init__(f'{text} {self.timeRemaining}', position)

    @staticmethod
    def _formatTime(seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"