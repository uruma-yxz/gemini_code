from src.Dto.InfoDto import InfoDto
from src.useCase.info.GetPath import GetPath
from src.useCase.info.GetOs import GetOs
from dataclasses import dataclass


@dataclass
class GetInfo:
    __getOs:GetOs
    __getPath:GetPath

    def execute(self)->InfoDto:
        return InfoDto(self.__getOs.execute(),self.__getPath.execute())

