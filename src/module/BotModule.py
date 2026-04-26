from dataclasses import dataclass

from src.Model.ResponseFromIA import ResponseFromIA
from src.port.Bot import Bot
from src.useCase.bot.PromptInitial import PromptInitial
from src.useCase.bot.SendPrompt import SendPrompt
from src.useCase.info import GetInfo
from src.utils.Spinner import Spinner
from colorama import Fore,Style


@dataclass
class BotModule:
    def __init__(self,bot:Bot,getInfo:GetInfo,):
        self.__sendPrompt = SendPrompt(bot)
        self.__promptInitial = PromptInitial(getInfo)
        pass
    
    async def sendPrompt(self,text:str)-> str:
        spinner = Spinner('Aguardando resposta do Gemini Code...')
        spinner.start()
        result:ResponseFromIA = await self.__sendPrompt.execute(text)
        spinner.succeed("Sucesso [+]")
        return result.response
    
    async def boot(self):
        await self.sendPrompt(self.__promptInitial.execute())
        while True:
            response = await self.sendPrompt(input("Envie a msg: "))
            print(response)