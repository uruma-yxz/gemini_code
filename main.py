import asyncio

from src.App import App

app = App()
asyncio.run(app.bootstrap())