import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from src.config import HEADERS


class BrowserEngine:
    def __init__(self):
        self.browser = None
        self.context = None
        # Инициализируем объект Stealth один раз
        self.stealth_config = Stealth()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

    async def start(self):
        """Запуск браузера в фоновом режиме."""
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )

    async def get_page_content(self, url: str, wait_time: int = 5000) -> str:
        page = await self.context.new_page()
        # Применяем стелс-режим к каждой странице
        # В предоставленном вами коде метод называется apply_stealth_async
        try:
            await self.stealth_config.apply_stealth_async(page)
        except Exception as e:
            print(f"Ошибка применения Stealth: {e}")

        try:
            # Для Google лучше использовать 'domcontentloaded'
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await asyncio.sleep(wait_time / 1000) # Реальная пауза
            return await page.content()
        except Exception as e:
            print(f"Ошибка: {e}")
            return ""
        finally:
            await page.close()

    async def stop(self):
        """Закрытие браузера."""
        if self.browser:
            await self.browser.close()
            await self.pw.stop()