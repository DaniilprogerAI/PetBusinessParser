from bs4 import BeautifulSoup
from src.config import EMAIL_REGEX, FREE_EMAIL_DOMAINS, CONTACT_KEYWORDS
import urllib.parse


def clean_email(email_raw: str) -> str:
    """Очищает email от маскировки и пробелов."""
    return email_raw.lower().replace("[at]", "@").replace(" ", "")


def extract_emails(html: str) -> set:
    """Находит все уникальные email в HTML коде."""
    emails = EMAIL_REGEX.findall(html)
    unique_emails = {clean_email(e) for e in emails}

    # Фильтруем B2B: убираем бесплатные домены
    return {e for e in unique_emails if e.split('@')[-1] not in FREE_EMAIL_DOMAINS}


def find_contact_links(html: str, base_url: str) -> list:
    """Ищет ссылки на страницы 'Контакты'."""
    soup = BeautifulSoup(html, 'lxml')
    contact_links = []

    for a in soup.find_all('a', href=True):
        href = a['href'].lower()
        if any(key in href for key in CONTACT_KEYWORDS):
            full_url = urllib.parse.urljoin(base_url, a['href'])
            contact_links.append(full_url)

    return list(set(contact_links))


def find_pdf_links(html: str, base_url: str) -> list:
    """Ищет ссылки на PDF-файлы (прайсы, каталоги)."""
    soup = BeautifulSoup(html, 'lxml')
    pdf_links = []

    for a in soup.find_all('a', href=True):
        href = a['href'].lower()
        if href.endswith('.pdf'):
            full_url = urllib.parse.urljoin(base_url, a['href'])
            pdf_links.append(full_url)

    return list(set(pdf_links))