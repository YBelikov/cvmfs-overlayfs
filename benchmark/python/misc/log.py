from enum import Enum

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    
class Logger:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def log(level, message):
        print(f'[{level.name}]: {message}')