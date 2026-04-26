from src.adapter.PlaywrightAdapter import PlaywrightAdapter
from src.Logo.Logo import logo
from colorama import Fore,Style
from halo import Halo
import os
import time


def bot():
    bot = PlaywrightAdapter()
    saveComent = input("Digita: ")
    spinner = Halo(text=' Processando...', spinner='dots', color='magenta')
    spinner.start()
    resultado = bot.execute(saveComent)
    spinner.succeed("Sucesso [+]")
    print(resultado.response)