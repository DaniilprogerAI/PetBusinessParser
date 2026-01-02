from src.storage import *
from src.scraper import *
from src.network import *
from src.classifier import BusinessClassifier

async def run_parser(urls):
    exporter = ExcelExporter()

    for url in urls:
        html = await fetch_html(url)
        if html:
            # 1. Ищем email
            emails = extract_emails(html)

            b_classifier = BusinessClassifier()

            niche = b_classifier.classify(html)

            # 2. Для каждого email создаем запись
            for email in emails:
                # В MVP название компании берем из домена или Title
                company_name = urlparse(url).netloc

                exporter.add_record(
                    company=company_name,
                    email=email,
                    website=url,
                    niche=niche,  # Пока заглушка
                    city="Unknown"  # Пока заглушка
                )

    exporter.save()
