from random import randint


# Исключения
class BoardException(Exception):
    pass


# во внутренней логике должно выходить BoardOutException,
# которое будет показывать выход за границу поля. Затем оно должно
# отлавливаться во внешней логике, выводя сообщение об этой ошибке пользователю

class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы выстрелили мимо поля'


# не удается поставить корабль на полу в случае неправильных точек
class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже сюда стреляли. Попробуйте снова'


# исключение для нормального размещения кораблей
class BoardWrongShipException(BoardException):
    pass


# Класс точек на поле.
class Dot:
    def __init__(self, x, y):
        self.x = x  # создаем аттрибуты класса Dot
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:

    def __init__(self, lenght, point, orient):
        self.lenght = lenght    # длина корабля
        self.point = point    # точка размещения носа корабля
        self.orient = orient    # ориентация
        self.life = lenght    # количество жизни равно длине

    # возвращает список всех точек корабля
    @property    # декоратор для неявного вызова
    def dots(self):
        ship_dots = []
        for i in range(self.lenght):
            # задаются координаты точек корабля с помощью новых переменных
            cur_x = self.point.x
            cur_y = self.point.y

            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            # переменная представляет собой список из кортежей с координатами корабля
            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:

    def __init__(self, hid=False, size=6):
        self.size = size  # размер доски
        self.ships = []  # список кораблей доски
        self.hid = hid  # переключатель скрыть/ показать корабли. Тип bool

        self.count = 0  # количество пораженных кораблей на доске

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []  # занятые точки или куда уже стреляли

    def __str__(self):  # вывод доски на печать
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:  # если доска скрыта, то для внешнего все меняется на ноль
            res = res.replace("■", "O")
        return res

    # для точки возвращает True, если она не выходит за пределы поля.
    def out(self, shot):
        return not ((0 <= shot.x < self.size) and (0 <= shot.y < self.size))

    # ставит корабль на доску.
    # Если ставить не удается, то следует исключение
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
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

    # делает выстрел по доске
    # если есть попытка выстрелить по неправильным координатам,
    # то выдает исключение
    def shot(self, d):
        if self.out(d):  # если выстрел мимо, то возникает исключение
            raise BoardOutException()

        if d in self.busy:  # если клетка занята, то возникает исключение
            raise BoardUsedException()

        self.busy.append(d)  # в ноормальном варианте занимаем клетку

        for ship in self.ships:
            if d in ship.dots:
                ship.life -= 1  # у корабля уменьшается жизнь
                self.field[d.x][d.y] = "X"  # на доску ставится крестик
                if ship.life == 0:
                    self.count += 1  # кол-во пораженных кораблей увеличивается
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
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    # спрашивает игрока в какую клетку он делает выстрел
    # обозначаем метод, реализация в потомках
    def ask(self):
        raise NotImplementedError()

    # делает ход в игре
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

    # класс игрока - человека


class User(Player):

    # метод запрашивает координаты из точки в консоли
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

    # класс компьютера с искусственным интеллектом


class AI(Player):

    # метод делает случайный выбор точки
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


# Основной класс
class Game:

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    # метод генерирует случайную доску
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    # проводится расстановка кораблей по полю
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]  # значения клеток кораблей
        board = Board(size=self.size)  # определяем объект доски для расстановки
        attempts = 0  # счетчик попыток

        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
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
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    # метод с самим игровым циклом
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
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


g = Game()
g.start()
