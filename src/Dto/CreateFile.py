from dataclasses import dataclass

@dataclass
class CreateFile:
    path:str
    content:str