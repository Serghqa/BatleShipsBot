import init_pole
from random import randint
from time import sleep

pole = init_pole.Pole()
pole.arrangement()


class Bot:
    def __init__(self):
        self.coords = [[(i, j) for j in range(10)] for i in range(10)]  # координаты поля
        self.coords_shots = {key: [] for key in range(10)}  # словарь хранения координат куда будут выстрелы
        self.count_ships = len(pole.ships_pole)  # количество кораблей на поле
        self.around_index = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)  # массив обхода /
        # координаты при попадании
        self.next_shots_find = (-1, 0), (0, -1), (0, 1), (1, 0)  # координаты для выстрела после 1 ранения корабля
        self.position_ship = None  # 1 - вертикальное, 2 - горизонтальное
        self.index_i = None  # координаты первого попадания по кораблю
        self.index_j = None  # координаты первого попадания по кораблю
        self.ship = None  # корабль по которому было попадание
        self.count_hit = 0  # счетчик попаданий по кораблю
        self.positive_indexes = None  # список координат после определения позиции корабля
        self.negative_indexes = None  # список координат после определения позиции корабля
        self.pos = False

    def set_shot_coords(self):  # создаем координаты выстрела
        if self.count_hit == 0:
            i = randint(0, 9)  # координата выстрела по оси x
            j = randint(0, 9)  # координата выстрела по оси y
            while True:
                if j not in self.coords_shots[i]:  # проверяем, что координата не повторяется
                    self.coords_shots.setdefault(i, []).append(j)  # добавим координату в список
                    return i, j
                i = randint(0, 9)
                j = randint(0, 9)
        elif self.count_hit == 1:
            i, j = self.next_shots_find[randint(0, 3)]
            l = len(self.coords[0])
            while True:
                if 0 <= self.index_i + i < l and 0 <= self.index_j + j < l:
                    if self.index_j + j not in self.coords_shots[self.index_i + i]:
                        self.coords_shots.setdefault(self.index_i + i, []).append(self.index_j + j)
                        return self.index_i + i, self.index_j + j
                i, j = self.next_shots_find[randint(0, 3)]
        else:
            if self.positive_indexes:
                i, j = self.positive_indexes.pop(0)  # получаем координаты /
                # больше координаты первого попадания
                self.coords_shots.setdefault(i, []).append(j)
                print(self.positive_indexes, self.index_i, self.index_j)
                return i, j
            elif self.negative_indexes:
                i, j = self.negative_indexes.pop(0)  # получаем координаты /
                # больше координаты первого попадания
                self.coords_shots.setdefault(i, []).append(j)
                print(self.negative_indexes, self.index_i, self.index_j)
                return i, j

    def add_around_index(self, i, j):  # функция добавления координат, где не может быть корабля
        l = len(self.coords[0])
        for x, y in self.around_index:
            if 0 <= i + x < l and 0 <= j + y < l:  # проверяем /
                # координату на возможный выход за пределы поля
                self.coords_shots.setdefault(i + x, []).append(j + y)  # добавляем координаты, на которых /
                # не может быть корабля

    def find_ship(self, i, j):
        for ship in pole.ships_pole:  # перебираем корабли
            if any(filter(lambda x: x == (i, j), ship.cell)):  # ищем корабль, которому принадлежит координата:
                return ship

    def determine_position_ship(self, i, j, x, y):  # функция определения позиции корабля (вертикальное\горизонтальное)
        if i != x:
            self.position_ship = 1  # вертикальное положение
        if j != y:
            self.position_ship = 2  # горизонтальное положение

    def add_around_ship_index(self, ship):  # функция добавления координат вокруг корабля
        for i, j in ship.cell:
            self.add_around_index(i, j)

    def set_list_shots(self):  # функция создания список добивания корабля
        lst_shots_pos = []  # положительный список
        lst_shots_neg = []  # отрицательный список
        len_ship = self.ship.lenght  # определяем длину возможного максимума списка
        for x in range(1, len_ship):
            if self.position_ship == 1:  # вертикальное положение корабля
                if self.index_i + x < len(self.coords[0]):
                    if self.index_j not in self.coords_shots[self.index_i + x]:
                        lst_shots_pos.append((self.index_i + x, self.index_j))
                if 0 <= self.index_i - x:
                    if self.index_j not in self.coords_shots[self.index_i - x]:
                        lst_shots_neg.append((self.index_i - x, self.index_j))
            elif self.position_ship == 2:
                if self.index_j + x < len(self.coords[0]):
                    if self.index_j + x not in self.coords_shots[self.index_i]:
                        lst_shots_pos.append((self.index_i, self.index_j + x))
                if 0 <= self.index_j - x:
                    if self.index_j - x not in self.coords_shots[self.index_i]:
                        lst_shots_neg.append((self.index_i, self.index_j - x))
        return lst_shots_pos, lst_shots_neg

    def check_hit(self, i, j):  # проверка попадания по кораблю
        if pole.pole[i][j] == '*':  # попадание
            self.count_hit += 1
            pole.pole[i][j] = '.'  # отобразим на экране попадание
            if self.count_hit == 1:  # если первое попадание
                self.ship = self.find_ship(i, j)  # получаем корабль по координатам выстрела
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                self.index_i, self.index_j = i, j  # обозначим координаты первого попадания
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    self.ship = None  # корабль уничтожен
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю

            elif self.count_hit == 2:  # второе попадание
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    self.ship = None  # корабль уничтожен
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                else:
                    self.determine_position_ship(self.index_i, self.index_j, i, j)  # определим позицию корабля
                    self.positive_indexes, self.negative_indexes = self.set_list_shots()  # создаем два списка /
                    # координат обстрела относительно положения корабля
                    self.pos = True
            else:
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    self.ship = None  # корабль уничтожен
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                    self.pos = False
        else:
            pole.pole[i][j] = 1  # обозначим промах на поле
            self.pos = False


bot = Bot()
count = 0
while bot.count_ships:
    i, j = bot.set_shot_coords()
    bot.check_hit(i, j)
    count += 1
    print(count)
    for x in pole.pole:
        print(*x, sep=' ')
    print('/' * 20)
    #sleep(5)