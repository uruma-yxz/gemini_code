from src.PromtBot.promtJson import promtJson
from src.adapter.PlaywrightAdapter import PlaywrightAdapter
from halo import Halo

def botPromt():
    promtInicial = promtJson()
    bot = PlaywrightAdapter()
    spinner = Halo(text=' Aguardando resposta do Gemini Code...', spinner='dots', color='magenta')
    spinner.start()
    resultado = bot.execute(promtInicial)
    spinner.succeed("Sucesso [+]")
    return resultado.response