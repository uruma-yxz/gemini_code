from dataclasses import dataclass

@dataclass
class ResponseFromIA:
    response:str
    time:str
    prompt:str
