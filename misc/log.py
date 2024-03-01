class Logger:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def log(level, message):
        print(f'[{level}]: {message}')


def log_error(message):
    print(f"[ERROR]: {message}")