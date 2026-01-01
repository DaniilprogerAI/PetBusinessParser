from src.storage import *

async def run_parser(urls):
    exporter = ExcelExporter()

    for url in urls:
        html = await fetch_html(url)
        if html:
            # 1. Ищем email
            emails = extract_emails(html)

            # 2. Для каждого email создаем запись
            for email in emails:
                # В MVP название компании берем из домена или Title
                company_name = urlparse(url).netloc

                exporter.add_record(
                    company=company_name,
                    email=email,
                    website=url,
                    niche="Veterinary",  # Пока заглушка
                    city="Unknown"  # Пока заглушка
                )

    exporter.save()
