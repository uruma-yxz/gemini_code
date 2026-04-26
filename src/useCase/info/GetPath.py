import os

class GetPath:
    def execute(self) -> str:
        file = os.getcwd()
        return file