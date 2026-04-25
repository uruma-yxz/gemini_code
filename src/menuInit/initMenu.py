from src.execut.bot import bot
from colorama import Fore,Style

def Menu():
    while True:
        bot()
        Continua = input(f"{Fore.RED}Quer Continua ?  [Sim | NAO]{Style.RESET_ALL} \n Digita: ").lower()
        if Continua in ["s","sim"]:
            continue
        elif Continua in ["n","nao"]:
            break