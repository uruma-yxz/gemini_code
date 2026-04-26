from halo import Halo

from src.Logo.ExibirLogo import ExibirLogo
from src.adapter.PlaywrightAdapter import PlaywrightAdapter
from src.module.BotModule import BotModule
from src.port.Bot import Bot
from src.useCase.bot.PromptInitial import PromptInitial
from src.useCase.info.GetOs import GetOs
from src.useCase.info.GetPath import GetPath
from src.useCase.info.GetInfo import GetInfo


class App:
    def __init__(self):
        ExibirLogo()
        self.__bot:Bot = PlaywrightAdapter()
        self.__getOs:GetOs = GetOs()
        self.__getPath:GetPath = GetPath()
        self.__getInfo:GetInfo = GetInfo(self.__getOs,self.__getPath)

    async def __modules(self):
        await BotModule(self.__bot,self.__getInfo).boot()

    
    async def bootstrap(self):
        await self.__modules()
