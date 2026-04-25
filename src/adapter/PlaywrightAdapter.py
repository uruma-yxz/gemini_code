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
        self.__user_data_dir = "/mnt/armario/gemini_code/user_session"
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
            execution_time = f"{time.time() - start_time:.2f}s"
            return ResponseFromIA(
                response=content,
                time=execution_time,
                prompt=prompt
            )
        except Exception as e:
            print(f"\nOcorreu um erro dentro do bot do gemini: {e}")
            return ResponseFromIA(
                response="Erro na execução",
                time="0s",
                prompt=prompt
            )
        finally:
            self.close()

    def __setup_environment(self):
        self.__verifyPath()
        self.__start_playwright()
        self.__createPersistentContext()
        return True

    def __start_playwright(self):
        instance = sync_playwright()
        started = instance.start()
        self.__playwright = started
        return self.__playwright

    def close(self):
        if self.__context:
            self.__context.close()
            self.__context = None
        if self.__playwright:
            self.__playwright.stop()
            self.__playwright = None

    def __verifyPath(self):
        path_exists = os.path.exists(self.__user_data_dir)
        if not path_exists:
            os.makedirs(self.__user_data_dir)
            return True
        return False

    def __createPersistentContext(self):
        self.__context = self.__playwright.chromium.launch_persistent_context(
            self.__user_data_dir,
            headless=False, 
            args=[
                "--start-maximized",
                "--disable-http2", 
                "--disable-dev-shm-usage" 
            ],
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        self.__page = self.__context.pages[0]

    def __gotoPage(self):
        target = self.__url
        strategy = "commit"
        limit = 60000
        self.__page.goto(
            target, 
            wait_until=strategy, 
            timeout=limit
        )

    def __insertPromptOnInput(self, prompt: str):
        selector = "div[role='textbox']"
        limit = 90000
        self.__page.wait_for_selector(selector, timeout=limit)
        self.__page.fill(selector, prompt)
        return True

    def __sendButton(self):
        selector = "button[aria-label='Enviar mensagem']"
        state_visible = "visible"
        self.__page.wait_for_selector(selector, state=state_visible)
        clickable_selector = f"{selector}:not([disabled])"
        self.__page.click(clickable_selector)

    def __getResponseFromGemini(self) -> str:
        container = ".markdown-main-panel"
        idle_selector = f"{container}[aria-busy='false']"
        limit = 90000
        self.__page.wait_for_selector(idle_selector, timeout=limit)
        result = self.__page.inner_text(container)
        return result

    def __intercept_route(self, route):
        req_url = route.request.url
        resource = route.request.resource_type
        blacklist_types = ["image", "font", "media"]
        blacklist_domains = ["google-analytics", "googletagmanager", "adservice"]
        is_blocked = resource in blacklist_types or any(d in req_url for d in blacklist_domains)
        if is_blocked:
            return route.abort()
        return route.continue_()
