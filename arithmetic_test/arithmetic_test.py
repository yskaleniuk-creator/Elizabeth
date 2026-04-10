import random


class ArithmeticQuiz:
    def __init__(self):
        # Названия уровней перефразированы
        self.levels = {
            1: "базовые вычисления (числа 2-9)",
            2: "квадраты двузначных чисел (11-29)"
        }
        self.score = 0
        self.difficulty = None

    def pick_level(self):
        while True:
            print("Укажите желаемую сложность:")
            for num, desc in self.levels.items():
                print(f"Вариант {num}: {desc}")

            choice = input("Ваш выбор: ").strip()
            if choice in ("1", "2"):
                self.difficulty = int(choice)
                break
            print("Ошибка: нужно напечатать 1 или 2.")

    def generate_task(self):
        if self.difficulty == 1:
            # Генерация примера для 1 уровня
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            op = random.choice(["+", "-", "*"])
            task_text = f"{a} {op} {b}"

            # Считаем результат без eval для надежности
            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            else:
                result = a * b

            return task_text, result
        else:
            # Генерация для 2 уровня
            base = random.randint(11, 29)
            return str(base), base ** 2

    def get_user_answer(self):
        while True:
            try:
                raw_val = input("Ответ: ")
                return int(raw_val)
            except ValueError:
                print("Пожалуйста, введите числовое значение.")

    def save_to_file(self):
        print("Записать ваши баллы в текстовый файл? (да/нет)")
        confirm = input(">> ").lower()
        if confirm in ("да", "д", "yes", "y"):
            name = input("Введите ваше имя: ")
            # Сохраняем согласно требованиям
            with open("results.txt", "a", encoding="utf-8") as f:
                log_info = (f"Студент: {name} | Результат: {self.score}/5 "
                            f"(Сложность: {self.difficulty})\n")
                f.write(log_info)
            print("Успешно сохранено в 'results.txt'.")

    def run(self):
        while True:
            self.score = 0
            self.pick_level()

            print(f"\nНачинаем тест. Уровень: {self.levels[self.difficulty]}")
            for i in range(5):
                q_text, correct_ans = self.generate_task()
                print(f"Вопрос №{i + 1}: {q_text} = ?")

                if self.get_user_answer() == correct_ans:
                    print("Правильно!")
                    self.score += 1
                else:
                    print(f"Неверно. Правильный ответ: {correct_ans}")

            print(f"\nИтог: {self.score} из 5 правильных ответов.")
            self.save_to_file()

            print("\nХотите пройти тест еще раз? (да/нет)")
            repeat = input(">> ").lower()
            if repeat not in ("да", "д", "yes", "y"):
                print("Работа завершена. Удачи!")
                break


if __name__ == "__main__":
    game = ArithmeticQuiz()
    game.run()