import time

import init_pole
from random import randint
from time import sleep


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
        self.positive_indexes = []  # список координат после определения позиции корабля
        self.negative_indexes = []  # список координат после определения позиции корабля
        self.min_len_ship = 1  # длина самого маленького(однопалубного) корабля

    def set_min_len_ship(self):
        self.min_len_ship = min(pole.ships_pole, key=lambda x: x.len_ship).len_ship  # определяем длину /
        # минимального корабля

    def check_meaning_shot(self, i, j):  # метод определения целесообразности выстрела
        l = len(self.coords[0])  # максимальный предел поля
        if self.min_len_ship == 1:  # если есть однопалубные корабли - есть смысл стрелять
            return True
        gor = 1  # счетчик вхождения минимального корабля относительно переданных координат по горизонту
        ver = 1  # счетчик вхождения минимального корабля относительно переданных координат по вертикали
        for x in range(1, self.min_len_ship):
            if j - x >= 0 and j - x not in self.coords_shots[i]:
                gor += 1
            else:
                break
        for x in range(1, self.min_len_ship):
            if j + x < l and j + x not in self.coords_shots[i]:
                gor += 1
            else:
                break
        for x in range(1, self.min_len_ship):
            if i - x >= 0 and j not in self.coords_shots[i - x]:
                ver += 1
            else:
                break
        for x in range(1, self.min_len_ship):
            if i + x < l and j not in self.coords_shots[i + x]:
                ver += 1
            else:
                break
        return self.min_len_ship <= gor or self.min_len_ship <= ver  # условие вхождения минимального корабля

    def set_shot_coords(self):  # создаем координаты выстрела
        if self.count_hit == 0:
            i = randint(0, 9)  # координата выстрела по оси x
            j = randint(0, 9)  # координата выстрела по оси y
            while True:
                if j not in self.coords_shots[i]:  # проверяем, что координата не повторяется
                    self.coords_shots.setdefault(i, []).append(j)  # добавим координату в список
                    if self.check_meaning_shot(i, j):  # проверка целесообразности выстрела по данным координатам
                        return i, j
                i = randint(0, 9)
                j = randint(0, 9)
        elif self.count_hit == 1:  # корабль ранен
            i, j = self.next_shots_find[randint(0, 3)]  # получаем случайную координату из возможных для /
            # добивания корвбля
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
                return i, j
            else:
                if self.negative_indexes:
                    i, j = self.negative_indexes.pop(0)  # получаем координаты /
                    # больше координаты первого попадания
                    self.coords_shots.setdefault(i, []).append(j)
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
        for i, j in ship.cell:  # перебираем координаты корабля
            self.add_around_index(i, j)  # добавим индексы вокруг координаты корабля в массив, чтобы игнорировать их /
            # в дальнейшем

    def set_list_shots(self):  # функция создания список добивания корабля
        len_ship = self.ship.len_ship  # определяем длину возможного максимума списка
        if self.position_ship == 1:  # вертикальное положение корабля
            for x in range(1, len_ship):
                if self.index_i + x < len(self.coords[0]):  # проверяем, что координата не выходит за пределы поля
                    if pole.pole[self.index_i + x][self.index_j] == 2:  # если координата второе попадание - игнорируем
                        continue
                    else:
                        if self.index_j not in self.coords_shots[self.index_i + x]:  # проверяем, что такой координаты /
                            # еще нет в массиве куда уже стреляли
                            self.positive_indexes.append((self.index_i + x, self.index_j))  # добавим в позитивный /
                            # список на добивание
                        else:
                            break  # иначе не имеет смысла дальше добавлять координаты
            for x in range(1, len_ship):
                if 0 <= self.index_i - x:
                    if pole.pole[self.index_i - x][self.index_j] == 2:
                        continue
                    else:
                        if self.index_j not in self.coords_shots[self.index_i - x]:
                            self.negative_indexes.append((self.index_i - x, self.index_j))
                        else:
                            break
        elif self.position_ship == 2:  # горизонтальное положение корабля
            for x in range(1, len_ship):
                if self.index_j + x < len(self.coords[0]):
                    if pole.pole[self.index_i][self.index_j + x] == 2:
                        continue
                    else:
                        if self.index_j + x not in self.coords_shots[self.index_i]:
                            self.positive_indexes.append((self.index_i, self.index_j + x))
                        else:
                            break
            for x in range(1, len_ship):
                if 0 <= self.index_j - x:
                    if pole.pole[self.index_i][self.index_j - x] == 2:
                        continue
                    else:
                        if self.index_j - x not in self.coords_shots[self.index_i]:
                            self.negative_indexes.append((self.index_i, self.index_j - x))
                        else:
                            break

    def check_hit(self, i, j):  # проверка попадания по кораблю
        if pole.pole[i][j] == '*':  # попадание
            self.count_hit += 1
            pole.pole[i][j] = self.count_hit  # отобразим на экране попадание
            if self.count_hit == 1:  # если первое попадание
                self.ship = self.find_ship(i, j)  # получаем корабль по координатам выстрела
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                self.index_i, self.index_j = i, j  # обозначим координаты первого попадания
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    pole.ships_pole.remove(self.ship)  # удалим корабль из списка
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                    if self.count_ships:  # проверим есть ли еще корабли на поле
                        self.set_min_len_ship()  # переопределим длину минимального корабля из оставшихся
                    self.ship = None  # корабль уничтожен

            elif self.count_hit == 2:  # второе попадание
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    pole.ships_pole.remove(self.ship)  # удалим корабль из списка
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                    if self.count_ships:  # проверим есть ли еще корабли на поле
                        self.set_min_len_ship()  # переопределим длину минимального корабля из оставшихся
                    self.ship = None  # корабль уничтожен
                else:
                    self.determine_position_ship(self.index_i, self.index_j, i, j)  # определим позицию корабля
                    self.set_list_shots()  # создаем два списка /
                    # координат обстрела относительно положения корабля

            else:
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    pole.ships_pole.remove(self.ship)  # удалим корабль из списка
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                    self.positive_indexes.clear()  # очистим позитивный список
                    self.negative_indexes.clear()  # очистим негативный список
                    if self.count_ships:  # проверим есть ли еще корабли на поле
                        self.set_min_len_ship()  # переопределим длину минимального корабля из оставшихся
                    self.ship = None  # корабль уничтожен
        else:
            pole.pole[i][j] = '#'  # обозначим промах на поле
            if self.count_hit > 1:  # проверим, что идет добивание по координатам из позитивного списка
                self.positive_indexes.clear()  # если промах по координатам позитивного списка, очистим его /
                # (он больше не нужен)

count = 0
for x in range(1):
    pole = init_pole.Pole()
    pole.arrangement()
    bot = Bot()
    while bot.count_ships:
        i, j = bot.set_shot_coords()
        bot.check_hit(i, j)
        count += 1
        print(i, j)
        for i in pole.pole:

            print(*i)
        print('-'*20)
        #time.sleep(5)
        #print(bot.min_len_ship)
print(count)