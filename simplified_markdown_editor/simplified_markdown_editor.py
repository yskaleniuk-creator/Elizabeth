class MarkdownGenerator:
    def __init__(self):
        self.doc_content = ""
        # Список доступных форматов
        self.tags = {
            "plain", "bold", "italic", "header", "link",
            "inline-code", "ordered-list", "unordered-list", "new-line"
        }
        # Управляющие команды
        self.control_cmds = {"!help", "!done", "exit"}

    def print_manual(self):
        print("Список доступных тегов: " + ", ".join(self.tags))
        print("Команды управления: !help — справка, !done — сохранить результат")

    def _get_row_number(self):
        while True:
            try:
                amount = int(input("Сколько строк добавить? "))
                if amount > 0:
                    return amount
                print("Введите число больше нуля.")
            except ValueError:
                print("Ошибка: требуется целое число.")

    def run_engine(self):
        print("--- Система подготовки Markdown-файлов активирована ---")
        print("Используйте !help для просмотра опций или exit для отмены.")

        while True:
            selection = input("\nВыберите формат или действие: ").strip().lower()

            if selection in self.control_cmds:
                if selection == "!help":
                    self.print_manual()
                elif selection == "!done":
                    with open("output.md", "w", encoding="utf-8") as target_file:
                        target_file.write(self.doc_content)
                    print("Файл output.md успешно сгенерирован. Программа завершена.")
                    break
                elif selection == "exit":
                    print("Работа завершена без записи данных.")
                    break
                continue

            if selection not in self.tags:
                print("Такого формата не существует. Попробуйте снова.")
                continue

            # Обработка различных типов разметки
            if selection == "plain":
                text_input = input("Текст: ")
                self.doc_content += text_input

            elif selection == "bold":
                text_input = input("Жирный текст: ")
                self.doc_content += f"**{text_input}**"

            elif selection == "italic":
                text_input = input("Курсивный текст: ")
                self.doc_content += f"*{text_input}*"

            elif selection == "inline-code":
                text_input = input("Код в строке: ")
                self.doc_content += f"`{text_input}`"

            elif selection == "header":
                while True:
                    try:
                        priority = int(input("Приоритет заголовка (1-6): "))
                        if 1 <= priority <= 6:
                            break
                        print("Допустимы значения только от 1 до 6.")
                    except ValueError:
                        print("Нужно ввести цифру.")
                text_input = input("Заголовок: ")
                self.doc_content += f"{'#' * priority} {text_input}\n"

            elif selection == "link":
                title = input("Текст ссылки: ")
                address = input("Адрес (URL): ")
                self.doc_content += f"[{title}]({address})"

            elif selection == "new-line":
                if self.doc_content.endswith("\n\n"):
                    pass
                elif self.doc_content.endswith("\n"):
                    self.doc_content += "\n"
                else:
                    self.doc_content += "\n\n"

            elif selection in ("ordered-list", "unordered-list"):
                total_items = self._get_row_number()
                if self.doc_content and not self.doc_content.endswith("\n"):
                    self.doc_content += "\n"

                for step in range(1, total_items + 1):
                    item_text = input(f"Содержимое пункта {step}: ")
                    if selection == "ordered-list":
                        self.doc_content += f"{step}. {item_text}\n"
                    else:
                        self.doc_content += f"* {item_text}\n"
                self.doc_content += "\n"

            # Предварительный просмотр
            print("\n>>> Предварительный просмотр документа:")
            print(self.doc_content)
            print(">>> Конец превью")


if __name__ == "__main__":
    app = MarkdownGenerator()
    app.run_engine()