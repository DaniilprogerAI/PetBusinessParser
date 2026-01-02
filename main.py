import asyncio
from src.orchestrator import ParserOrchestrator

if __name__ == "__main__":
    # Тестовый список сайтов (в реальности будет грузиться из файла или поиска)
    test_urls = [
        "https://example-vet-clinic.pl",
        "https://zoo-shop-warszawa.pl",
        "https://groomer-krakow.com"
    ]

    orchestrator = ParserOrchestrator(test_urls, max_concurrent=5)

    print("🚀 Запуск парсера...")
    asyncio.run(orchestrator.run())
    print("✅ Работа завершена. Проверьте папку data/results.xlsx")
