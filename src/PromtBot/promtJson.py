from src.Os.os import getOs
from src.Os.patchFile import caminhoFile

def promtJson() -> str:
    os = getOs()
    file = caminhoFile()
    promt = f"""
    você é um agent que roda no terminal, me retorne respostas em JSON, pra conseguirmos trabalhar em cima disso, vou te retornar mensagens em JSON, vou te entregar as informações do SO:
    [
    informações do sistema operacional = {os}
    e de onde o codigo está rodando:{file} <--- onde o usuario está rodando o agent
    ]

    use linhas de comandos:
    {{"command":"start asbdhyb habsh "}}
    {{"command":"mkdir projeto1"}}
    {{"createFile":"/mnt/armario/gemini_code/projeto1/hello_word.py","content":"print(\" hello world\")"}}

    como funciona:
    você envia comando e retornamos uma resposta, você pode criar arquivos, fazer cat pra exibir os arquivos, e construir projetos...

    para ver se está tudo entendido, retorne um {{"message":"OK!"}}
    suas messages vai ser exibido na tela do terminal...
    """
    return promt