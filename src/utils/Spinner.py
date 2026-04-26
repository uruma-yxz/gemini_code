from halo import Halo

class Spinner:
    def __init__(self,text:str):
        self.__spinner = Halo(text=text, spinner='dots', color='magenta')
        pass 
    
    def start(self)->None:
        self.__spinner.start()
        pass

    def succeed(self,text:str)-> None:
        self.__spinner.succeed(text)
        return
