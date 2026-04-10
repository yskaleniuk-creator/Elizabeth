class MatrixProcessor:
    def __init__(self, data_grid):
        self.grid = data_grid
        self.rows_cnt = len(data_grid)
        self.cols_cnt = len(data_grid[0]) if self.rows_cnt > 0 else 0

    def show_matrix(self):
        for row in self.grid:
            # Форматирование вывода: округление до 2 знаков, убираем лишние нули
            print(' '.join(f"{round(elem, 2):g}" for elem in row))

    def add_matrix(self, other):
        if self.rows_cnt != other.rows_cnt or self.cols_cnt != other.cols_cnt:
            print("[!] Ошибка: Матрицы должны быть одинакового размера.")
            return None

        sum_res = [[self.grid[y][x] + other.grid[y][x] for x in range(self.cols_cnt)]
                   for y in range(self.rows_cnt)]
        return MatrixProcessor(sum_res)

    def multiply_by_scalar(self, k):
        scaled_res = [[item * k for item in row] for row in self.grid]
        return MatrixProcessor(scaled_res)

    def multiply_matrices(self, second_matrix):
        if self.cols_cnt != second_matrix.rows_cnt:
            print("[!] Ошибка: Несоответствие размерностей для умножения.")
            return None

        # Классическое умножение матриц
        output = [[sum(self.grid[i][z] * second_matrix.grid[z][j] for z in range(self.cols_cnt))
                   for j in range(second_matrix.cols_cnt)] for i in range(self.rows_cnt)]
        return MatrixProcessor(output)

    def apply_rotation(self, mode=1):
        if mode == 1:
            # Транспонирование (главная диагональ)
            transformed = [[self.grid[j][i] for j in range(self.rows_cnt)] for i in range(self.cols_cnt)]
        elif mode == 2:
            # Отражение по побочной диагонали
            transformed = [[self.grid[self.rows_cnt - 1 - j][self.cols_cnt - 1 - i]
                            for j in range(self.rows_cnt)] for i in range(self.cols_cnt)]
        elif mode == 3:
            # Зеркало по вертикали
            transformed = [line[::-1] for line in self.grid]
        elif mode == 4:
            # Зеркало по горизонтали
            transformed = self.grid[::-1]
        else:
            print("Указанный тип модификации не найден.")
            return None
        return MatrixProcessor(transformed)

    def calculate_determinant(self):
        if self.rows_cnt != self.cols_cnt:
            print("[!] Ошибка: Определитель ищется только в квадратных матрицах.")
            return None
        return self._recursive_det(self.grid)

    def _recursive_det(self, current_mtx):
        n = len(current_mtx)
        if n == 1:
            return current_mtx[0][0]
        if n == 2:
            return current_mtx[0][0] * current_mtx[1][1] - current_mtx[0][1] * current_mtx[1][0]

        det_value = 0
        for col_idx in range(n):
            # Создаем минор
            minor = [line[:col_idx] + line[col_idx + 1:] for line in current_mtx[1:]]
            det_value += ((-1) ** col_idx) * current_mtx[0][col_idx] * self._recursive_det(minor)
        return det_value

    def invert(self):
        main_det = self.calculate_determinant()
        if main_det == 0 or main_det is None:
            print("Матрица вырожденная (Det=0), инверсия невозможна.")
            return None

        size = self.rows_cnt
        complements = []
        for r in range(size):
            comp_row = []
            for c in range(size):
                # Поиск минора для алгебраического дополнения
                minor_matrix = [l[:c] + l[c + 1:] for idx, l in enumerate(self.grid) if idx != r]
                comp_row.append(((-1) ** (r + c)) * self._recursive_det(minor_matrix))
            complements.append(comp_row)

        # Транспонируем матрицу дополнений и делим на детерминант
        inverted_grid = [[complements[j][i] / main_det for j in range(size)] for i in range(size)]
        return MatrixProcessor(inverted_grid)


def get_user_matrix():
    while True:
        try:
            dims = input("Укажите размерность (строк и столбцов): ").split()
            rows, cols = map(int, dims)
            break
        except Exception:
            print("Некорректный ввод. Нужно два целых числа.")

    data = []
    print(f"Заполнение данных ({rows} строк):")
    for i in range(rows):
        while True:
            raw_row = input(f"Строка №{i + 1}: ").split()
            if len(raw_row) != cols:
                print(f"Нужно ввести {cols} чисел.")
                continue
            try:
                data.append([float(x) for x in raw_row])
                break
            except ValueError:
                print("Обнаружены нечисловые символы.")
    return MatrixProcessor(data)


def start_console_interface():
    while True:
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Сложить матрицы")
        print("2. Масштабировать (на число)")
        print("3. Произведение двух матриц")
        print("4. Изменить ориентацию (транспонирование)")
        print("5. Найти детерминант")
        print("6. Обратная матрица")
        print("0. Выход")

        user_choice = input("Выберите пункт: ")

        if user_choice == '1':
            a, b = get_user_matrix(), get_user_matrix()
            res = a.add_matrix(b)
            if res:
                print("Результат сложения:")
                res.show_matrix()

        elif user_choice == '2':
            a = get_user_matrix()
            while True:
                try:
                    num = float(input("Множитель: "))
                    break
                except ValueError:
                    print("Введите число.")
            res = a.multiply_by_scalar(num)
            print("Матрица после умножения:")
            res.show_matrix()

        elif user_choice == '3':
            a, b = get_user_matrix(), get_user_matrix()
            res = a.multiply_matrices(b)
            if res:
                print("Результат перемножения:")
                res.show_matrix()

        elif user_choice == '4':
            print("Режимы: 1-Главная, 2-Побочная, 3-Лево/Право, 4-Верх/Низ")
            try:
                m_type = int(input("Режим: "))
                mat = get_user_matrix()
                res = mat.apply_rotation(m_type)
                if res:
                    print("Обновленная матрица:")
                    res.show_matrix()
            except ValueError:
                print("Требуется номер режима.")

        elif user_choice == '5':
            mat = get_user_matrix()
            d = mat.calculate_determinant()
            if d is not None:
                print(f"Детерминант равен: {round(d, 4)}")

        elif user_choice == '6':
            mat = get_user_matrix()
            res = mat.invert()
            if res:
                print("Инвертированная матрица:")
                res.show_matrix()

        elif user_choice == '0':
            print("Завершение работы...")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    start_console_interface()