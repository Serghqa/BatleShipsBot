from random import randint


class Ship:
    def __init__(self, lenght, tp, x=None, y=None):
        """Инициализация корабля"""
        self.lenght = lenght  # длина корабля
        self.tp = tp  # расположение корабля (tp = 1 - горизонтальное, tp = 2 - вертикальное)
        self.x = x
        self.y = y
        self.cell = [0 for i in range(lenght)]  # список для хранения координат корабля
        self.destroyed = False  # флаг уничтожения корабля
        self.counter = lenght  # счетчик палуб корабля

    def set_start_coords(self, x, y):
        """Начало координат корабля"""
        self.x = x
        self.y = y

    def get_start_coords(self):
        """Координата начала корабля"""
        return self.x, self.y

    def out_pole(self):
        """Проверка выхода корабля за пределы поля"""
        x, y = self.get_start_coords()  # получение начала координат корабля
        if self.tp == 1:
            return 0 <= x and x + self.lenght < 10 and 0 <= y < 10
        if self.tp == 2:
            return 0 <= y and y + self.lenght < 10 and 0 <= x < 10


class Pole:
    def __init__(self):
        """Инициализация поля"""
        self.pole = [[0 for j in range(10)] for i in range(10)]  # инициализация игрового поля 10х10
        self.ships_pole = []  # список, который будет хранить корабли после расстановки их на поле

    def arrangement(self):
        """Расстановка кораблей рандомно на поле"""
        ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), \
                 Ship(3, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), \
                 Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), \
                 Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), \
                 Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2))]
        ship = ships.pop(0)
        while True:
            ship.set_start_coords(randint(0, 9), randint(0, 9))  # рандомно создаем начальную координату первого корабля
            if ship.out_pole():  # проверяем не выходит ли корабль за пределы игрового поля
                self.ships_pole.append(ship)  # после удачных проверок добавляем корабль в список для хранения
                x = ship.x
                y = ship.y
                if ship.tp == 1:
                    for i in range(ship.lenght):
                        self.pole[y][x + i] = '*'  # расставляем корабль на игровом поле
                        ship.cell[i] = (y, x + i)  # сохраняем координаты корабля в список
                if ship.tp == 2:
                    for i in range(ship.lenght):
                        self.pole[y + i][x] = '*'  # расставляем корабль на игровом поле
                        ship.cell[i] = (y + i, x)  # сохраняем координаты корабля в список
                break
        while ships:  # пока все корабли не будут расставлены на игровом поле
            ship = ships.pop(0)
            while True:
                ship.set_start_coords(randint(0, 9), randint(0, 9))  # создаем рандомно начало координат корабля
                if ship.out_pole():  # проверяем не выходит ли корабль за пределы игрового поля
                    if not self.is_collide(
                            ship):  # проверяем, не пересекается ли наш корабль с уже расставленными кораблями на поле
                        self.ships_pole.append(ship)  # после успешных проверок добавляем корабль в список на хранение
                        x = ship.x
                        y = ship.y
                        if ship.tp == 1:
                            for i in range(ship.lenght):
                                self.pole[y][x + i] = '*'  # расставляем корабль на игровое поле
                                ship.cell[i] = (y, x + i)  # сохраняем координаты корабля в список
                        if ship.tp == 2:
                            for i in range(ship.lenght):
                                self.pole[y + i][x] = '*'  # расставляем корабль на игровое поле
                                ship.cell[i] = (y + i, x)  # сохраняем координаты корабля в список
                        break

    def check_collide(self, i, j):
        """Проверка координаты корабля на пересечение с другим кораблем"""
        if self.pole[i][j] == '*':
            return True
        if i + 1 < 10:
            if self.pole[i + 1][j] == '*':
                return True
        if i - 1 >= 0:
            if self.pole[i - 1][j] == '*':
                return True
        if j + 1 < 10:
            if self.pole[i][j + 1] == '*':
                return True
        if j - 1 >= 0:
            if self.pole[i][j - 1] == '*':
                return True
        if i - 1 >= 0 and j - 1 >= 0:
            if self.pole[i - 1][j - 1] == '*':
                return True
        if i + 1 < 10 and j + 1 < 10:
            if self.pole[i + 1][j + 1] == '*':
                return True
        if i + 1 < 10 and j - 1 >= 0:
            if self.pole[i + 1][j - 1] == '*':
                return True
        if i - 1 >= 0 and j + 1 < 10:
            if self.pole[i - 1][j + 1] == '*':
                return True
        return False  # координата корабля не пересекается с другими

    def is_collide(self, ship):
        """Проверка столкновения (пересечения) кораблей"""
        x = ship.x
        y = ship.y
        flag = False
        if ship.tp == 1:
            for i in range(y, y + 1):
                for j in range(x, x + ship.lenght):
                    if self.check_collide(i, j):
                        flag = True  # корабль пересекается, проверка не прошла
                        return flag
        if ship.tp == 2:
            for i in range(y, y + ship.lenght):
                for j in range(x, x + 1):
                    if self.check_collide(i, j):
                        flag = True  # корабль пересекается, проверка не прошла
                        return flag
        return flag  # корабль прошел проверку (пересечений с другими кораблями нет)
