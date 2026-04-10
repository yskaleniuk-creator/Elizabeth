import random


class RockPaperGame:
    DEFAULT_ITEMS = ["rock", "paper", "scissors"]

    # Статусы приложения
    STATUS_WAIT = 0
    STATUS_PLAY = 1
    STATUS_OFF = 2

    def __init__(self, storage_path: str = "rating.txt"):
        self.file_name = storage_path
        self.player_name = ""
        self.score = 0
        self.options = self.DEFAULT_ITEMS.copy()
        self.state = self.STATUS_WAIT

    def _load_user_data(self) -> None:
        """Считывание прогресса из файла."""
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                for line in f:
                    name, val = line.strip().split()
                    if name == self.player_name:
                        self.score = int(val)
                        return
        except (FileNotFoundError, ValueError):
            pass
        self.score = 0

    def setup_player(self) -> None:
        self.player_name = input("Введите ваше имя:\n> ").strip()
        print(f"Добро пожаловать, {self.player_name}!")
        self._load_user_data()
        self.show_help()

    def show_help(self):
        print("Команды управления:")
        print("!start   - начать поединок")
        print("!rating  - показать мои очки")
        print("!exit    - выйти из приложения")
        print("Чтобы сменить правила, введите свои варианты через запятую (до старта).")

    def config_variants(self, text: str) -> None:
        clean_text = text.strip()
        if not clean_text:
            self.options = self.DEFAULT_ITEMS.copy()
        else:
            self.options = [x.strip() for x in clean_text.split(",")]
        print("Список жестов успешно изменен.")

    def _check_result(self, user_move: str, bot_move: str) -> bool:
        """Определяет, проиграл ли человек (логика циклического списка)."""
        idx = self.options.index(user_move)
        # Перестраиваем список так, чтобы выбор игрока был в центре
        rotated = self.options[idx + 1:] + self.options[:idx]
        # Половина списка после выбора игрока — это то, чему он проигрывает
        half = len(rotated) // 2
        return bot_move in rotated[:half]

    def play_round(self, user_choice: str) -> None:
        bot_choice = random.choice(self.options)

        if bot_choice == user_choice:
            print(f"Ничья! Оба выбрали {bot_choice}")
            self.score += 50
        elif self._check_result(user_choice, bot_choice):
            print(f"Увы, поражение. Бот показал {bot_choice}")
        else:
            print(f"Победа! {bot_choice} слабее, чем ваш выбор")
            self.score += 100

    def _handle_input(self, msg: str):
        # Глобальные команды
        if msg == "!exit":
            print("Выход из игры... До новых встреч!")
            self.state = self.STATUS_OFF
            return

        if msg == "!rating":
            print(f"Ваш счет на данный момент: {self.score}")
            return

        # Действия в меню
        if self.state == self.STATUS_WAIT:
            if msg == "!help":
                self.show_help()
            elif msg == "!start":
                print("Бой начался! Вводите ваш жест.")
                self.state = self.STATUS_PLAY
            else:
                self.config_variants(msg)

        # Действия в процессе игры
        elif self.state == self.STATUS_PLAY:
            if msg in self.options:
                self.play_round(msg)
            else:
                print("Неизвестный жест. Используйте варианты из списка или !exit.")

    def launch(self):
        self.setup_player()

        while self.state != self.STATUS_OFF:
            user_msg = input("> ").strip()
            if not user_msg:
                continue
            self._handle_input(user_msg)


if __name__ == "__main__":
    game_instance = RockPaperGame()
    game_instance.launch()