import customtkinter as ctk
import asyncio
import threading
from src.orchestrator import ParserOrchestrator


class ParserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ВЕТ-Парсер B2B (Польша)")
        self.geometry("600x500")

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Заголовок и ввод
        self.label = ctk.CTkLabel(self, text="Введите URL сайтов (каждый с новой строки):", font=("Arial", 14))
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.url_input = ctk.CTkTextbox(self, height=150)
        self.url_input.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        # 2. Лог событий
        self.log_output = ctk.CTkTextbox(self, height=150, state="disabled", fg_color="black", text_color="green")
        self.log_output.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # 3. Кнопка запуска
        self.start_button = ctk.CTkButton(self, text="ЗАПУСТИТЬ СБОР", command=self.start_thread)
        self.start_button.grid(row=3, column=0, padx=20, pady=20)

    def write_log(self, message):
        """Метод для вывода сообщений в консоль интерфейса."""
        self.log_output.configure(state="normal")
        self.log_output.insert("end", f"> {message}\n")
        self.log_output.configure(state="disabled")
        self.log_output.see("end")

    def start_thread(self):
        """Запуск парсера в отдельном потоке, чтобы GUI не зависал."""
        urls = self.url_input.get("1.0", "end-1c").split("\n")
        urls = [u.strip() for u in urls if u.strip()]

        if not urls:
            self.write_log("Ошибка: Список URL пуст!")
            return

        self.start_button.configure(state="disabled")
        threading.Thread(target=self.run_async_logic, args=(urls,), daemon=True).start()

    def run_async_logic(self, urls):
        """Обертка для запуска асинхронного оркестратора."""
        self.write_log(f"Запуск... Целей обнаружено: {len(urls)}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        orchestrator = ParserOrchestrator(urls)
        loop.run_until_complete(orchestrator.run())

        self.write_log("Готово! Результаты сохранены в data/results.xlsx")
        self.start_button.configure(state="normal")


if __name__ == "__main__":
    app = ParserApp()
    app.mainloop()