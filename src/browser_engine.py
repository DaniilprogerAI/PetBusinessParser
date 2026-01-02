import asyncio
from playwright.async_api import async_playwright
from src.config import HEADERS


class BrowserEngine:
    def __init__(self):
        self.browser = None
        self.context = None

    async def start(self):
        """Запуск браузера в фоновом режиме."""
        self.pw = await async_playwright().start()
        # Используем chromium для максимальной совместимости
        self.browser = await self.pw.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent=HEADERS["User-Agent"],
            viewport={'width': 1920, 'height': 1080}
        )

    async def get_page_content(self, url: str, wait_time: int = 5000) -> str:
        """Загружает страницу, исполняет JS и возвращает финальный HTML."""
        if not self.context:
            await self.start()

        page = await self.context.new_page()
        try:
            # Переход на сайт с ожиданием загрузки сети [cite: 35, 67]
            await page.goto(url, timeout=30000, wait_until="networkidle")

            # Дополнительное ожидание для подгрузки динамических элементов
            await page.wait_for_timeout(wait_time)

            content = await page.content()
            return content
        except Exception as e:
            print(f"Playwright error for {url}: {e}")
            return ""
        finally:
            await page.close()

    async def stop(self):
        """Закрытие браузера."""
        if self.browser:
            await self.browser.close()
            await self.pw.stop()