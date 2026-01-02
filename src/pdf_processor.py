import fitz  # PyMuPDF
import httpx
import io
from src.scraper import extract_emails


class PDFExtractor:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    async def get_emails_from_pdf(self, pdf_url: str) -> set:
        """Скачивает PDF и извлекает из него email-адреса."""
        emails = set()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(pdf_url, timeout=self.timeout)
                if response.status_code == 200:
                    # Открываем PDF прямо из потока байтов
                    with fitz.open(stream=io.BytesIO(response.content), filetype="pdf") as doc:
                        text = ""
                        for page in doc:
                            text += page.get_text()

                        # Используем уже готовый метод из scraper.py
                        emails = extract_emails(text)
        except Exception as e:
            print(f"Ошибка при обработке PDF {pdf_url}: {e}")

        return emails