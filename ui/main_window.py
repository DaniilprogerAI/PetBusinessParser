import customtkinter as ctk
import asyncio
import threading
from src.orchestrator import ParserOrchestrator
from src.discovery import GoogleDiscovery
from src.browser_engine import BrowserEngine
from src.config import POLISH_CITIES  # Берем города из конфига


class ParserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ВЕТ-Парсер B2B: Авто-сбор")
        self.geometry("700x600")

        # 1. Выбор ниши
        self.label_niche = ctk.CTkLabel(self, text="Выберите нишу для сбора:", font=("Arial", 14))
        self.label_niche.pack(pady=(20, 5))

        self.niche_selector = ctk.CTkOptionMenu(self, values=[
            "Veterinary", "Pet Shop", "Grooming", "Shelter/Foundation"
        ])
        self.niche_selector.pack(pady=5)

        # 2. Настройка глубины поиска (страниц Google на каждый город)
        self.label_pages = ctk.CTkLabel(self, text="Глубина поиска (страниц на город):")
        self.label_pages.pack(pady=(10, 0))
        self.pages_slider = ctk.CTkSegmentedButton(self, values=["1", "2", "3"])
        self.pages_slider.set("1")
        self.pages_slider.pack(pady=5)

        # 3. Кнопка запуска
        self.start_button = ctk.CTkButton(
            self, text="ЗАПУСТИТЬ АВТО-ПОИСК ПО ВСЕЙ ПОЛЬШЕ",
            command=self.start_thread,
            fg_color="green", hover_color="darkgreen"
        )
        self.start_button.pack(pady=20)

        # 4. Лог событий
        self.log_output = ctk.CTkTextbox(self, height=250, state="disabled", fg_color="black", text_color="#00FF00")
        self.log_output.pack(padx=20, pady=10, fill="both", expand=True)

    def write_log(self, message):
        self.log_output.configure(state="normal")
        self.log_output.insert("end", f"> {message}\n")
        self.log_output.configure(state="disabled")
        self.log_output.see("end")

    def start_thread(self):
        """Запуск процесса в отдельном потоке."""
        niche = self.niche_selector.get()
        num_pages = int(self.pages_slider.get())

        self.start_button.configure(state="disabled")
        # Передаем параметры напрямую в метод
        threading.Thread(target=self.run_async_logic, args=(niche, num_pages), daemon=True).start()

    def run_async_logic(self, niche, num_pages):
        """Оркестрация поиска по городам и парсинга."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def full_process():
            browser = BrowserEngine()
            await browser.start()
            discovery = GoogleDiscovery(browser)

            # Словарь для формирования поискового запроса на польском
            search_queries = {
                "Veterinary": "klinika weterynaryjna",
                "Pet Shop": "sklep zoologiczny",
                "Grooming": "groomer fryzjer dla psów",
                "Shelter/Foundation": "schronisko dla zwierząt"
            }

            base_query = search_queries.get(niche, "weterynarz")
            all_found_urls = set()

            # Итерируемся по списку городов из config.py
            # Для MVP возьмем первые 5 городов, чтобы не заблокировал Google
            cities_to_scan = list(POLISH_CITIES)[:5]

            for city in cities_to_scan:
                current_query = f"{base_query} {city}"
                self.write_log(f"🔎 Поиск в городе: {city.capitalize()}...")

                urls = await discovery.search_business_urls(current_query, num_pages)
                all_found_urls.update(urls)
                await asyncio.sleep(2)  # Пауза, чтобы Google не выдал капчу

            self.write_log(f"✅ Всего найдено уникальных сайтов: {len(all_found_urls)}")

            if all_found_urls:
                self.write_log("🚀 Начинаю извлечение email и классификацию...")
                orchestrator = ParserOrchestrator(list(all_found_urls))
                orchestrator.browser = browser  # Переиспользуем браузер
                await orchestrator.run()

            await browser.stop()
            self.write_log("🏁 Сбор завершен! Данные в data/results.xlsx")
            self.start_button.configure(state="normal")

        loop.run_until_complete(full_process())


if __name__ == "__main__":
    app = ParserApp()
    app.mainloop()