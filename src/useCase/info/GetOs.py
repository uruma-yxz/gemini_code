import platform


class GetOs:
    def execute(self) -> str:
        name_Os = platform.release()
        return name_Os