import asyncio
import logging
from urllib.parse import urlparse
from src.network import fetch_html
from src.scraper import extract_emails, find_contact_links, find_pdf_links
from src.classifier import BusinessClassifier
from src.geo_extractor import GeoExtractor
from src.pdf_processor import PDFExtractor
from src.browser_engine import BrowserEngine
from src.storage import ExcelExporter

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ParserOrchestrator:
    def __init__(self, urls, max_concurrent=5):
        self.urls = urls
        self.semaphore = asyncio.Semaphore(max_concurrent)  # Ограничение потоков
        self.exporter = ExcelExporter()
        self.classifier = BusinessClassifier()
        self.geo = GeoExtractor()
        self.pdf_tool = PDFExtractor()
        self.browser = BrowserEngine()

    async def process_site(self, url):
        """Полный цикл обработки одного сайта."""
        async with self.semaphore:
            logging.info(f"Начало обработки: {url}")

            # 1. Быстрая попытка через HTTPX
            html = await fetch_html(url)

            # 2. Если пусто или JS-сайт — включаем Playwright
            if not html or "javascript" in html.lower() or "root" in html.lower():
                logging.info(f"Используем браузер для: {url}")
                html = await self.browser.get_page_content(url)

            if not html:
                return

            # 3. Сбор данных с главной страницы
            emails = extract_emails(html)
            niche = self.classifier.classify(html)
            city = self.geo.extract_city(html)

            # 4. Поиск и обход страниц контактов (если на главной нет email)
            if not emails:
                contact_links = find_contact_links(html, url)
                for link in contact_links[:2]:  # Проверяем максимум 2 страницы контактов
                    c_html = await fetch_html(link)
                    emails.update(extract_emails(c_html))

            # 5. Поиск и парсинг PDF (прайсов)
            pdf_links = find_pdf_links(html, url)
            for pdf in pdf_links[:3]:  # Проверяем до 3 PDF файлов
                pdf_emails = await self.pdf_tool.get_emails_from_pdf(pdf)
                emails.update(pdf_emails)

            # 6. Сохранение результатов
            if emails:
                company_name = urlparse(url).netloc
                for email in emails:
                    self.exporter.add_record(
                        company=company_name,
                        email=email,
                        website=url,
                        niche=niche,
                        city=city
                    )
                logging.info(f"Найдено {len(emails)} email для {url}")

    async def run(self):
        """Запуск всей очереди задач."""
        await self.browser.start()
        tasks = [self.process_site(url) for url in self.urls]
        await asyncio.gather(*tasks)
        await self.browser.stop()
        self.exporter.save()