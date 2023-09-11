import init_pole
from random import randint

pole = init_pole.Pole()
pole.arrangement()


class Bot:
    def __init__(self):
        self.coords = [[(i, j) for j in range(10)] for i in range(10)]  # координаты поля
        self.coords_shots = {}  # координаты куда уже стреляли
        self.count_ships = len(pole.ships_pole)  # количество кораблей на поле

    def set_shot_coords(self):  # создаем координаты выстрела
        i = randint(0,9)  # координата выстрела по оси x
        j = randint(0,9)  # координата выстрела по оси y
        while True:
            if j not in self.coords_shots[i]:  # проверяем, что координата не повторяется
                self.coords_shots.setdefault(i, []).append(j)  # добавим координату в список
                return i, j
            i = randint(0, 9)
            j = randint(0, 9)

    def check_hit(self, i, j):  # проверка попадания по кораблю
        i, j = i, j
        if pole.pole[i][j] == '*':  # попадание
            for ship in pole.ships_pole:  # перебираем корабли
                if any(filter(lambda x: x == (i, j), ship.cell)):  # ищем корабль, которому принадлежит координата
                    pole.pole[i][j] = -1  # отобразим на экране попадание
                    ship.counter -= 1  # уменьшаем очки прочности корабля
                    if ship.counter == 0:
                        pole.ships_pole.remove(ship)  # уничтожаем корабль если его прочность равна 0
                        self.count_ships -= 1  # уменьшаем счетчик количества кораблей
        pole.pole[i][j] = 1



bot = Bot()