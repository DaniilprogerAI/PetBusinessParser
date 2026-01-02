import re

# Список бесплатных почтовых сервисов (для фильтрации B2B)
FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
    "wp.pl", "onet.pl", "interia.pl", "o2.pl", "gazeta.pl", "tlen.pl"
}

# Ключевые слова для поиска страниц контактов (на польском и английском)
CONTACT_KEYWORDS = ["kontakt", "contact", "about", "o-nas", "biuro", "mapa"]

# Ключевые слова для классификации ниш [cite: 62]
NICHES = {
    "vet": ["weterynarz", "klinika", "lecznica", "przychodnia"],
    "shop": ["sklep", "zoo", "akwarystyka", "karma"],
    "grooming": ["strzyżenie", "groomer", "fryzjer dla psów"],
    "shelter": ["schronisko", "fundacja", "azyl", "przytulisko"]
}

# Регулярное выражение для поиска email [cite: 42, 43]
# Учитывает базовую маскировку (напр. "info [at] domain.com")
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9_.+-]+(?:\s*\[at\]\s*|\s*@\s*)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
)

# Настройки User-Agent для имитации браузера
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Ключевые слова для классификации ниш [cite: 8-13, 62]
NICHES_KEYWORDS = {
    "Veterinary": [
        "weterynarz", "weterynarii", "klinika weterynaryjna", "lecznica",
        "przychodnia weterynaryjna", "chirurgia zwierząt", "szczepienia", "veterinary"
    ],
    "Pet Shop": [
        "sklep zoologiczny", "karma dla psa", "akcesoria dla zwierząt",
        "gryzaki", "legowiska", "akwarystyka", "pet shop", "zoology"
    ],
    "Grooming": [
        "groomer", "strzyżenie psów", "fryzjer dla psów", "kąpiel psa",
        "pielęgnacja zwierząt", "grooming", "trymowanie"
    ],
    "Shelter/Foundation": [
        "schronisko", "przytulisko", "fundacja dla zwierząt", "adopcja psa",
        "azyl", "shelter", "stowarzyszenie"
    ],
    "Manufacturing": [
        "producent karmy", "produkcja akcesoriów", "hurtownia zoologiczna",
        "distribution", "factory", "wytwórnia"
    ],
    "Breeder": [
        "hodowla psów", "hodowla kotów", "szczenięta", "kennel", "breeding"
    ]
}

# Регулярное выражение для польского почтового индекса (напр. 00-001)
PL_ZIP_REGEX = re.compile(r"(\d{2}-\d{3})")

# Список крупнейших городов Польши для валидации [cite: 5]
POLISH_CITIES = {
    "warszawa", "kraków", "krakow", "łódź", "lodz", "wrocław", "wroclaw",
    "poznań", "poznan", "gdańsk", "gdansk", "szczecin", "bydgoszcz",
    "lublin", "białystok", "bialystok", "katowice", "gdynia", "częstochowa"
}