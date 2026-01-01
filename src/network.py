import httpx
import logging
from config import *

async def fetch_html(url: str, timeout: int = 10) -> str:
    """Загружает HTML содержимое страницы."""
    async with httpx.AsyncClient(follow_redirects=True, headers=HEADERS) as client:
        try:
            response = await client.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.text
            logging.warning(f"Ошибка {response.status_code} для {url}")
        except Exception as e:
            logging.error(f"Не удалось загрузить {url}: {e}")
    return ""