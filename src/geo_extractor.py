import re
from bs4 import BeautifulSoup
from src.config import PL_ZIP_REGEX, POLISH_CITIES


class GeoExtractor:
    def extract_city(self, html: str) -> str:
        """
        Ищет город в тексте страницы.
        Приоритет: Почтовый индекс -> Список городов.
        """
        soup = BeautifulSoup(html, 'lxml')
        # Ищем в футере или блоке address, так как там самая высокая концентрация данных
        search_area = ""
        for tag in ['footer', 'address', 'header']:
            element = soup.find(tag)
            if element:
                search_area += " " + element.get_text()

        if not search_area:
            search_area = soup.get_text()

        # Метод 1: Поиск по почтовому индексу (самый точный для Польши)
        zip_match = PL_ZIP_REGEX.search(search_area)
        if zip_match:
            # Берем текст после индекса (обычно там город)
            start_index = zip_match.end()
            after_zip = search_area[start_index:start_index + 30].strip()
            # Очищаем от лишних символов и берем первое слово
            potential_city = re.split(r'[,.\s\n]', after_zip)[0]
            if potential_city:
                return potential_city.capitalize()

        # Метод 2: Поиск по списку городов (если индекс не найден)
        text_lower = search_area.lower()
        for city in POLISH_CITIES:
            if city in text_lower:
                return city.capitalize()

        return "Unknown"