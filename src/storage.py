import pandas as pd
from datetime import datetime
import os
from urllib.parse import urlparse


class ExcelExporter:
    def __init__(self, output_path="data/results.xlsx"):
        self.output_path = output_path
        # Поля согласно ТЗ [cite: 52-60]
        self.columns = [
            "Компания", "Email", "Сайт", "Ниша",
            "Страна", "Город", "Дата сбора", "Доменная зона"
        ]
        self.data = []

    def add_record(self, company, email, website, niche, city, country="Poland"):
        """Добавляет одну запись в список."""
        # Извлекаем доменную зону для аналитики [cite: 60]
        domain_zone = urlparse(website).netloc.split('.')[-1] if website else ""

        record = {
            "Компания": company,
            "Email": email,
            "Сайт": website,
            "Ниша": niche,
            "Страна": country,  # [cite: 5, 57]
            "Город": city,
            "Дата сбора": datetime.now().strftime("%Y-%m-%d"),  # [cite: 23, 59]
            "Доменная зона": domain_zone
        }
        self.data.append(record)

    def save(self):
        """Сохраняет накопленные данные в Excel с фильтрацией."""
        if not self.data:
            print("Нет данных для сохранения.")
            return

        df = pd.DataFrame(self.data)

        # 1. Удаление дубликатов по Email [cite: 45, 46]
        df = df.drop_duplicates(subset=['Email'], keep='first')

        # 2. Проверка существования папки
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # 3. Сохранение в Excel
        try:
            df.to_excel(self.output_path, index=False, engine='openpyxl')
            print(f"Файл успешно сохранен: {self.output_path}")
            print(f"Всего уникальных B2B контактов: {len(df)}")
        except Exception as e:
            print(f"Ошибка при сохранении Excel: {e}")