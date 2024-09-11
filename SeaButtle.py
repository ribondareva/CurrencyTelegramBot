import random  # Импортируем модуль random для генерации случайных чисел

class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates  # Сохраняем координаты корабля

    def get_coordinates(self):
        return self.coordinates  # Возвращаем координаты корабля
class Board:
    def __init__(self):
        self.size = 6  # Устанавливаем размер доски 6x6
        self.grid = [["О" for _ in range(self.size)] for _ in range(self.size)]  # Инициализируем доску
        self.ships = []  # Список для хранения объектов кораблей

    def display(self):
        header = " | " + " | ".join(str(i) for i in range(1, self.size + 1)) + " |"  # Заголовок
        print(header)  # Вывод заголовка
        for index, row in enumerate(self.grid):
            print(f"{index + 1} | " + " | ".join(row) + " |")  # Выводим содержимое доски

    def place_ship(self, length):
        placed = False  # Переменная для отслеживания успешности размещения
        while not placed:
            orientation = random.choice(['H', 'V'])  # Случайная ориентация
            if orientation == 'H':  # Если корабль горизонтальный
                x = random.randint(0, self.size - 1)  # Случайная строка
                y = random.randint(0, self.size - length)  # Случайный столбец
                if self.can_place_ship(x, y, length, orientation):
                    coordinates = [(x, y + i) for i in range(length)]  # Генерируем координаты корабля
                    ship = Ship(coordinates)  # Создаем объект корабля
                    self.ships.append(ship)  # Добавляем корабль в список
                    for coord in coordinates:
                        self.grid[coord[0]][coord[1]] = '■'  # Помечаем клетки
                    placed = True  # Успех: корабль размещен
            else:  # Если вертикальный
                x = random.randint(0, self.size - length)  # Случайный столбец
                y = random.randint(0, self.size - 1)  # Случайная строка
                if self.can_place_ship(x, y, length, orientation):
                    coordinates = [(x + i, y) for i in range(length)]  # Генерируем координаты
                    ship = Ship(coordinates)  # Создаем объект корабля
                    self.ships.append(ship)  # Добавляем корабль в список
                    for coord in coordinates:
                        self.grid[coord[0]][coord[1]] = '■'  # Помечаем клетки
                    placed = True  # Успех: корабль размещен

    def can_place_ship(self, x, y, length, orientation):
        for i in range(length):
            if orientation == 'H':
                if self.grid[x][y + i] != 'О':  # Проверка занятости
                    return False
                # Проверяем соседние клетки
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= x + dx < self.size and 0 <= y + i + dy < self.size:
                            if self.grid[x + dx][y + i + dy] == '■':
                                return False
            else:
                if self.grid[x + i][y] != 'О':
                    return False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= x + i + dx < self.size and 0 <= y + dy < self.size:
                            if self.grid[x + i + dx][y + dy] == '■':
                                return False
        return True

    def setup_ships(self):
        self.place_ship(3)  # Размещаем один корабль длиной 3
        for _ in range(2):
            self.place_ship(2)  # Размещаем два корабля длиной 2
        for _ in range(4):
            self.place_ship(1)  # Размещаем четыре корабля длиной 1

    def shoot(self, coordinates):
        x, y = coordinates
        if self.grid[x][y] == '■':  # Если попали в корабль
            self.grid[x][y] = "X"  # Помечаем попадание
            return True
        elif self.grid[x][y] == "X" or self.grid[x][y] == "T":
            raise ValueError("Повторный выстрел")
        else:  # Промах
            self.grid[x][y] = "T"  # Помечаем промах
            return False

    def is_game_over(self):
        return all(cell != '■' for row in self.grid for cell in row)  # Проверка на отсутствие кораблей

class Game:
    def __init__(self):
        self.computer_board = Board()  # Создаем доску для компьютера
        self.player_board = Board()  # Создаем доску для игрока
        self.setup_boards()  # Настраиваем доски

    def setup_boards(self):
        self.computer_board.setup_ships()  # Корабли компьютера
        self.player_board.setup_ships()  # Корабли игрока

    def computer_turn(self):
        while True:
            x, y = random.randint(0, 5), random.randint(0, 5)  # Случайные координаты
            try:
                if self.player_board.shoot((x, y)):
                    print(f"Компьютер попал в {x + 1}, {y + 1}!")  # Уведомляем о попадании
                else:
                    print(f"Компьютер промахнулся в {x + 1}, {y + 1}.")  # Уведомляем о промахе
                break  # Завершаем цикл после одного хода
            except ValueError:
                continue  # Повторный выстрел, пробуем снова

    def player_turn(self):
        while True:
            try:
                x = int(input("Введите координату X (1-6): ")) - 1  # -1 для индексации
                y = int(input("Введите координату Y (1-6): ")) - 1  # -1 для индексации
                result = self.computer_board.shoot((x, y))  # Выстрел игрока
                if result:
                    print(f"Вы попали в {x + 1}, {y + 1}!")  # Попадание
                else:
                    print(f"Вы промахнулись в {x + 1}, {y + 1}.")  # Промах
                break  # Завершаем цикл после одного хода
            except ValueError:
                print("Неверный ввод. Попробуйте еще раз.")  # Неверный ввод
            except IndexError:
                print("Координаты должны быть в пределах 1-6. Попробуйте снова!")  # Проверка границ

    def play(self):
        while True:
            print("\nДоска компьютера:")
            self.computer_board.display()  # Показываем доску компьютера

            self.player_turn()  # Ход игрока
            if self.computer_board.is_game_over():  # Проверка на победу
                print("Вы выиграли! Поздравляем!")  # Поздравляем игрока
                break  # Завершаем игру

            print("\nДоска игрока:")
            self.player_board.display()  # Показываем доску игрока

            self.computer_turn()  # Ход компьютера
            if self.player_board.is_game_over():  # Проверка на победу компьютера
                print("Компьютер выиграл! Попробуйте снова.")  # Сообщаем о победе компьютера
                break  # Завершаем игру
# Пример запуска игры
if __name__ == "__main__":
    game = Game()  # Создаем экземпляр игры
    game.play()  # Запускаем игровую сессию