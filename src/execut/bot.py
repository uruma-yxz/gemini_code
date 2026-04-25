from src.adapter.PlaywrightAdapter import PlaywrightAdapter
from src.Logo.Logo import logo
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def bot():
    bot = PlaywrightAdapter()
    print(logo())
    saveComent = input("Digita: ")
    time.sleep(0.5)
    resultado = bot.execute(saveComent)
    print(resultado.response)
    time.sleep(1)   