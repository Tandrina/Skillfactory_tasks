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

class Ship:

    def __init__(self, lenght, point, orient, life ):
        self.lenght = lenght
        self.point = point
        self.orient = orient
        self.life = life

    # возвращает список всех точек корабля
    @property
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

    def __init__(self, coord, ships, hid = False, count = 6):
        self.coord = coord  # список клеток, занимаемых кораблем
        self.ships = ships  # список кораблей доски
        self.hid = hid  # переключатель скрыть/ показать корабли. Тип bool
        self.count = count  # количество пораженных кораблей на доске

        self.field = [["O"] * coord for _ in range(coord)]

        self.busy = 0    # занятые точки или куда уже стреляли

    def __str__(self):    # вывод доски на печать
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid:
            res = res.replace("■", "O")
        return res

    # определяем не выходит ли точка за пределы доски
    def out(self, shot):
        return not((0<= shot.x < self.size) and (0<= shot.y < self.size))

    def attack(self.shot):
        if self.out(shot):
            raise BoardOutException
        
        if shot in self.busy:
            raise BoardUsedException

        #если ошибки не возникло, то добавляем в использованное
        self.busy.append(shot)    



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
    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    # Выводим доску в консоль в зависимости от флажка hid
    def show_board(self)

    # для точки возвращает True, если она не выходит за пределы поля.
    # иначе False:
    def out(self):

    # делает выстрел по доске
    # если есть попытка выстрелить по неправильным координатам,
    # то выдает исключение
    def shot(self):


# Внешняя логика

# общий класс игрока
class Player:
    def __init__(self, UserBoard, AiBoard):
        self.UserBoard = UserBoard
        self.AiBoard = AiBoard

    # спрашивает игрока в какую клетку он делает выстрел
    # обозначаем метод, реализация в потомках
    def ask(self):

    # делает ход в игре
    def move(self):

    # класс игрока - человека
    class User(Player):

        # метод запрашивает координаты из точки в консоли
        def ask(self):

    # класс компьютера с искусственным интеллектом
    class AI(Player):

        # метод делает случайный выбор точки
        def ask(self):

# Основной класс
class Game:

    def __init__(self, user, boardUser, AiPlayer, AiBoard):
        self.user = user
        self.boardUser = boardUser
        self.AiPlayer = AiPlayer
        self.AiBoard = AiBoard

    # метод генерирует случайную доску
    def random_board(self):


    # метод, приветствующий пользователя в консоли
    # и рассказывающий о формате ввода
    def greet(self):


    # метод с самим игровым циклом
    def loop(self):

    # запуск игры
    def start(self):

