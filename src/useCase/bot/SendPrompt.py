from src.Model.ResponseFromIA import ResponseFromIA

class SendPrompt:
    def __init__(self, bot):
        self.__bot = bot

    async def execute(self, prompt: str) -> ResponseFromIA:
        # Isso aqui SÓ funciona se o bot.execute for 'async def'
        return await self.__bot.execute(prompt)