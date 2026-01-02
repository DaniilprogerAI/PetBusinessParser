import asyncio
from bs4 import BeautifulSoup
from src.browser_engine import BrowserEngine
import urllib.parse


class GoogleDiscovery:
    def __init__(self, browser_engine: BrowserEngine):
        self.browser = browser_engine

    async def search_business_urls(self, query: str, num_pages: int = 1) -> list:
        """Ищет сайты компаний в Google по запросу."""
        all_links = set()

        for page in range(num_pages):
            # Формируем URL поиска (start=0, 10, 20...)
            start = page * 10
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"

            html = await self.browser.get_page_content(search_url, wait_time=3000)
            if not html:
                continue

            soup = BeautifulSoup(html, 'lxml')

            # В Google ссылки на сайты обычно лежат в тегах <div class="yuRUbf"> или <a> внутри h3
            for link in soup.select('div.yuRUbf a, div.g a'):
                href = link.get('href')
                if href and "http" in href and "google.com" not in href:
                    # Чистим ссылку до главного домена (опционально)
                    domain = f"{urllib.parse.urlparse(href).scheme}://{urllib.parse.urlparse(href).netloc}"
                    all_links.add(domain)

        return list(all_links)