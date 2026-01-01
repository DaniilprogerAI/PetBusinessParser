from bs4 import BeautifulSoup
from src.config import NICHES_KEYWORDS


class BusinessClassifier:
    def __init__(self):
        self.keywords = NICHES_KEYWORDS

    def clean_text(self, html: str) -> str:
        """Извлекает чистый текст из HTML для анализа."""
        soup = BeautifulSoup(html, 'lxml')
        # Удаляем скрипты и стили, чтобы не ловить ложные срабатывания
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text().lower()

    def classify(self, html: str) -> str:
        """
        Определяет нишу на основе весов ключевых слов[cite: 62].
        Возвращает 'Other', если совпадений мало.
        """
        text = self.clean_text(html)
        scores = {niche: 0 for niche in self.keywords.keys()}

        for niche, words in self.keywords.items():
            for word in words:
                if word in text:
                    # Считаем количество вхождений слова
                    scores[niche] += text.count(word)

        # Выбираем нишу с максимальным баллом
        best_niche = max(scores, key=scores.get)

        # Если совпадений нет или их слишком мало (порог 2), ставим 'Other'
        if scores[best_niche] < 2:
            return "Other / General Pet Business"

        return best_niche