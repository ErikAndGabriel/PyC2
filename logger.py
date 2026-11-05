import time
from .config import CINZA, RESET


def log(msg, cor=CINZA):
    hora = time.strftime("%H:%M:%S")
    print(f"{cor}[{hora}] {msg}{RESET}")
