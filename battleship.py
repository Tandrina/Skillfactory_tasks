from random import randint

# Исключения
class BoardException(Exception):
    pass


# во внутренней логике должно выходить BoardOutException,
# которое будет показывать выход за границу поля. Затем оно должно
# отлавливаться во внешней логике, выводя сообщение об этой ошибке пользователю

class BoardOutException(BoardException):
    def __str__(self):
        return  'Вы выстрелили мимо поля'

# не удается поставить корабль на полу в случае неправильных точек
class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже сюда стреляли. Попробуйте снова'

# точка указана рядом с кораблем. Неверное значение.
class BoardKontur(BoardException):
    def __str__(self):
        return 'Неверное значение. Корабли не могут стоять так близко'

class BoardWrongShipException(BoardException):
    pass


# Класс точек на поле.
class Dot:
    def __init__(self, x, y):
        self.x = x    # создаем аттрибуты класса Dot
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


# Класс всех кораблей
class Ship:

    def __init__(self, lenght, point, orient, life ):
        self.length = lenght   # длина корабля
        self.point = point   # точка носа корабля
        self.orient = orient   # ориентация вертикаль/ горизонталь
        self.life = life

    # возвращает список все точки, которые есть у корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            # задаются координаты точек корабля с помощью новых переменных
            cur_x = self.point.x
            cur_y = self.point.y

            # проверка ориентации корабля
            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            # переменная представляет собой список из кортежей с координатами корабля
            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    # показывает поражен корабль или нет
    def shooten(self, shot):
        return shot in self.dots

class Board:

    def __init__(self, hid = False, size = 6):
        self.size = size  # размер клеток доски
        self.hid = hid  # переключатель скрыть/ показать корабли. Тип bool

        self.count = 0  # количество пораженных кораблей на доске

        self.field = [[" "] * size for _ in range(size)]

        self.ships = []  # список кораблей доски
        self.busy = []    # занятые точки или куда уже стреляли

    # метод создания корабля
    # Если ставить не удается, то следует исключение
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d):
                raise BoardWrongShipException()
            elif d in self.busy:
                raise BoardUsedException()

        for d in ship.dots:  # заполнение ячейки новым символом
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    # Обводит корабль по контуру.
    # Помечает соседние с кораблем точки, где поставить нельзя
    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):    # вывод доски на печать
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:  # если доска скрыта, то все заполненные поля закрываются пробелами
            res = res.replace("■", " ")
        return res

    # определяем не выходит ли точка за пределы доски
    def out(self, shot):
        return not((0<= shot.x < self.size) and (0<= shot.y < self.size))

    def shot(self.shot):
        if self.out(shot):
            raise BoardOutException

        if shot in self.busy:
            raise BoardUsedException

        #если ошибки не возникло, то добавляем в использованное
        self.busy.append(shot)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
            if ship.lives == 0:
                self.count += 1
                self.contour(ship, verb=True)
                print("Корабль уничтожен!")
                return False
        else:
            print("Корабль ранен!")
            return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False


    def begin(self):
        self.busy = []

# Внешняя логика

# общий класс игрока
class Player:
    def __init__(self, UserBoard, AiBoard):
        self.UserBoard = UserBoard
        self.AiBoard = AiBoard

    # спрашивает игрока в какую клетку он делает выстрел
    # обозначаем метод, реализация в потомках
    def ask(self):
        raise NotImplementedError()

    # делает ход в игре
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.AiBoard.shot(target)
                return repeat
            except BoardException as e:
                print(e)

# класс игрока - человека
class User(Player):

    # метод запрашивает координаты из точки в консоли
    def ask(self):
        while True:
            cords = input("Ваш ход (через пробел): ").split()

            if len(cords) != 2:  # петля проверки количества знаков
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):  # проверка на тип данных (целое число)
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

    # класс компьютера с искусственным интеллектом
class AI(Player):

    # метод делает случайный выбор точки
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

# Основной класс
class Game:

    # метод генерирует случайную доску
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board
        co = self.random_board
        co.hid = True

        self.AI = AI(co, pl)
        self.User = User(pl, co)

    @property
    def random_board(self):   # петля. Пока не будет создана доска, ее создание будет запрашиваться
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
    # метод, приветствующий пользователя в консоли
    # и рассказывающий о формате ввода
    def greet(self):
        print('Добро пожаловать на игру!')
        print('Перед вами доска')
        print('делайте ход, вводя координаты клетки через пробел')
        print('x - номер строки')
        print('у - номер столбка')

    # процесс работы игры
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.User.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.AI.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    # запуск игры
    def start(self):
        self.greet()
        self.loop()
