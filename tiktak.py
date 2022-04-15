cell_num = list(range(1, 10))  # задаем список из диапазона для создания доски


def main():  # Создаем основной каркас игры
    print('Приветствую Вас на игре "Крестики - нолики')
    print('В ней побеждает тот, кто первым заполнит линейку из трех клеток одним символом')
    print('Удачи в сражении!')
    print('Бой начинается!')

    counter = 0    # создаем счетчик количества ходов
    board(cell_num)
    symbol_1 = 'X'
    symbol_2 = 'O'

    xo = choice()    # вы выбираете знак, вывод на печать
    print(f'Вы выбрали {xo}.')
    print('Первым ходит Х')

    win = False
    while not win:    # цикл передачи хода
        board(cell_num)
        if counter % 2 == 0:
            player_1(symbol_1)
        else:
            player_2(symbol_2)
        counter += 1

        if 3 <= counter < 9:  # после третьего шага начинается проверка на выигрыш. Если да, то игра прекращается.
            if is_winner(cell_num):
                print('Вы выиграли!')
                break

        if counter == 9:  # если счетчик набирает 9 и не произошло выигрыша, то объявляется ничья. Игра прекращается.
            print("Ничья!")
            break


def board(cell_num):  # вывод доски на печать при старте или передаче хода
    print(f'-------------')

    for i in range(3):
        print(f'| {cell_num[0 + i * 3]} | {cell_num[1 + i * 3]} | {cell_num[2 + i * 3]} |')
        print(f'-------------')

    return 'Доска для игры сейчас'


# игрок выбирает крестик или нолик.
# от этого определяется будет он игроком 1 или игроком 2


def choice():
    symbol = ' '
    while not (symbol == "X" or symbol == "O"):
        symbol = input('Вы выбираете X или О? \n').upper()

    if symbol == 'X':
        symbol_1 = 'X'
        return symbol_1

    if symbol == 'O':
        symbol_2 = 'O'
        print()
        return symbol_2


# игрок задает номер ячейки
# проводится проверка на диапазон от 1 до 9
# проверка на свободную ячейку
# если проверки удачны, то символ записывается в ячейку и данные пердаются на выход


def player_1(symbol_1):
    correct = False
    while not correct:
        print('Ходит крестик')
        move = input('Введите номер ячейки: \n')
        try:    # ловушка на ввод не числа
            move = int(move)
        except ValueError:
            print('Вы не ввели число. Попробуйте снова.')
            continue

        except TypeError:
            print('Вы не ввели число. Попробуйте снова.')

        try:    # ловушка на выход за границу диапазона
            if 1 > move > 9:
                raise ValueError()

        except ValueError:
            print("Вы ввели неверное число")
            continue

        if 1 <= move <= 9:
            if (str(cell_num[move - 1])) not in "XO":
                cell_num[move - 1] = symbol_1
                print('Ход переходит к другому игроку')
                correct = True

            else:
                print('Ячейка занята. Выберте другую')


# игрок задает номер ячейки
# проводится проверка на диапазон от 1 до 9
# проверка на свободную ячейку
# если проверки удачны, то символ записывается в ячейку и данные пердаются на выход


def player_2(symbol_2):
    correct = False
    while not correct:
        print('Ходит нолик')
        move = int(input('Введите номер ячейки: \n'))
        try:    # ловушка на ввод не числа
            move = int(move)
        except ValueError:
            print('Вы не ввели число. Попробуйте снова.')
            continue

        except TypeError:
            print('Вы не ввели число. Попробуйте снова.')
            continue

        try:    # ловушка на выход за границу диапазона
            if 1 > move > 9:
                raise ValueError("Вы ввели неверное число")

        except ValueError:
            print("Вы ввели неверное число")
            continue

        if 1 <= move <= 9:
            if (str(cell_num[move - 1])) not in "XO":
                cell_num[move - 1] = symbol_2
                print('Ход переходит к другому игроку')
                correct = True

            else:
                print('Ячейка занята. Выберте другую')


# проводится проверка на выигрыш


def is_winner(cell_num):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for i in win_coord:
        if cell_num[i[0]] == cell_num[i[1]] == cell_num[i[2]]:
            return cell_num[i[0]]
    return False


if __name__ == '__main__':
    main()
