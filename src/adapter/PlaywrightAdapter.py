import os
import time
from playwright.sync_api import sync_playwright
from src.Model.ResponseFromIA import ResponseFromIA
from src.port.Bot import Bot


class PlaywrightAdapter(Bot):
    def __init__(self):
        self.__playwright = None
        self.__context = None
        self.__page = None
        current_path = os.path.abspath(__file__)
        self.__user_data_dir = os.path.join(os.path.dirname(current_path), "user_session")
        self.__url = "https://gemini.google.com/app"

    def execute(self, prompt: str) -> ResponseFromIA:
        start_time = time.time()
        try:
            self.__setup_environment()
            self.__page.route("**/*", self.__intercept_route)
            self.__gotoPage()
            self.__insertPromptOnInput(prompt)
            self.__sendButton()
            content = self.__getResponseFromGemini()
            exec_time = f"{time.time() - start_time:.2f}s"
            return ResponseFromIA(response=content, time=exec_time, prompt=prompt)
        except Exception as e:
            print(f"\nOcorreu um erro dentro do bot do gemini: {e}")
            return ResponseFromIA(response="Erro na execução", time="0s", prompt=prompt)
        finally:
            self.close()

    def __setup_environment(self):
        self.__verifyPath()
        self.__start_playwright()
        self.__createPersistentContext()
        return True

    def __start_playwright(self):
        instance = sync_playwright()
        self.__playwright = instance.start()
        return self.__playwright

    def close(self):
        if self.__context:
            self.__context.close()
        if self.__playwright:
            self.__playwright.stop()

    def __verifyPath(self):
        if not os.path.exists(self.__user_data_dir):
            os.makedirs(self.__user_data_dir)

    def __createPersistentContext(self):
        self.__context = self.__playwright.chromium.launch_persistent_context(
            self.__user_data_dir,
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1920,1080"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        self.__page = self.__context.pages[0]

    def __gotoPage(self):
        self.__page.goto(self.__url, wait_until="commit", timeout=60000)
        self.__page.wait_for_selector("div[role='textbox']", timeout=30000)

    def __insertPromptOnInput(self, prompt: str):
        selector = "div[role='textbox']"
        self.__page.wait_for_selector(selector, timeout=60000)
        self.__page.fill(selector, prompt)
        return True

    def __sendButton(self):
        selector = "button[aria-label='Enviar mensagem']"
        try:
            self.__page.wait_for_selector(selector, timeout=10000)
            self.__page.eval_on_selector(selector, "el => el.click()")
        except:
            self.__page.keyboard.press("Enter")
        return True

    def __getResponseFromGemini(self) -> str:
        timeout = 90
        check_interval = 2
        last_text = ""
        for _ in range(int(timeout / check_interval)):
            time.sleep(check_interval)
            script = """
            () => {
                const nodes = document.querySelectorAll('.markdown, .message-content, [data-message-author-role="assistant"]');
                return nodes.length > 0 ? nodes[nodes.length - 1].innerText : "";
            }
            """
            current_text = self.__page.evaluate(script)
            if current_text and current_text == last_text:
                return current_text
            last_text = current_text
        return last_text if last_text else "Falha total na captura."

    def __intercept_route(self, route):
        bad = ["google-analytics", "googletagmanager", "adservice"]
        if route.request.resource_type in ["image", "font"] or any(d in route.request.url for d in bad):
            return route.abort()
        return route.continue_()