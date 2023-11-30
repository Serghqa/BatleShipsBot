import init_pole
from random import randint


class Bot:
    """Класс создания и управления ботом"""
    def __init__(self, obj, name='Bot'):
        self.name = name
        self.coords = [[(i, j) for j in range(10)] for i in range(10)]  # координаты поля
        self.coords_shots = {key: [] for key in range(10)}  # словарь хранения координат куда будут выстрелы
        self.count_ships = len(obj.ships_pole)  # количество кораблей на поле
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

    def set_min_len_ship(self, obj):
        """Определение длины минимального корабля (количество палуб)"""
        self.min_len_ship = min(obj.ships_pole, key=lambda x: x.len_ship).len_ship  # определяем длину /
        # минимального корабля

    def check_meaning_shot(self, i, j):
        """Метод определения целесообразности выстрела"""
        l: int = len(self.coords[0])  # максимальный предел поля
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

    def set_shot_coords(self):
        """Метод определения координаты выстрела"""
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
            # добивания корабля
            l: int = len(self.coords[0])
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

    def add_around_index(self, i, j):
        """Метод добавления координат, где не может быть корабля"""
        l = len(self.coords[0])
        for x, y in self.around_index:
            if 0 <= i + x < l and 0 <= j + y < l:  # проверяем /
                # координату на возможный выход за пределы поля
                self.coords_shots.setdefault(i + x, []).append(j + y)  # добавляем координаты, на которых /
                # не может быть корабля

    @staticmethod
    def find_ship(i, j, obj):
        """Поиск и возвращение корабля по координатам"""
        for ship in obj.ships_pole:  # перебираем корабли
            if any(filter(lambda x: x == (i, j), ship.cell)):  # ищем корабль, которому принадлежит координата:
                return ship

    def determine_position_ship(self, i, j, x, y):
        """Метод определения позиции корабля (вертикальное, горизонтальное)"""
        if i != x:
            self.position_ship = 1  # вертикальное положение
        if j != y:
            self.position_ship = 2  # горизонтальное положение

    def add_around_ship_index(self, ship):
        """Метод добавления координат вокруг корабля"""
        for i, j in ship.cell:  # перебираем координаты корабля
            self.add_around_index(i, j)  # добавим индексы вокруг координаты корабля в массив, чтобы игнорировать их /
            # в дальнейшем

    def set_list_shots(self, obj):
        """Создание списка с координатами для добивания корабля"""
        len_ship = self.ship.len_ship  # определяем длину возможного максимума списка
        if self.position_ship == 1:  # вертикальное положение корабля
            for x in range(1, len_ship):
                if self.index_i + x < len(self.coords[0]):  # проверяем, что координата не выходит за пределы поля
                    if obj.pole[self.index_i + x][self.index_j] == 2:  # если координата второе попадание - игнорируем
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
                    if obj.pole[self.index_i - x][self.index_j] == 2:
                        continue
                    else:
                        if self.index_j not in self.coords_shots[self.index_i - x]:
                            self.negative_indexes.append((self.index_i - x, self.index_j))
                        else:
                            break
        elif self.position_ship == 2:  # горизонтальное положение корабля
            for x in range(1, len_ship):
                if self.index_j + x < len(self.coords[0]):
                    if obj.pole[self.index_i][self.index_j + x] == 2:
                        continue
                    else:
                        if self.index_j + x not in self.coords_shots[self.index_i]:
                            self.positive_indexes.append((self.index_i, self.index_j + x))
                        else:
                            break
            for x in range(1, len_ship):
                if 0 <= self.index_j - x:
                    if obj.pole[self.index_i][self.index_j - x] == 2:
                        continue
                    else:
                        if self.index_j - x not in self.coords_shots[self.index_i]:
                            self.negative_indexes.append((self.index_i, self.index_j - x))
                        else:
                            break

    def check_hit(self, i, j, obj):
        """Проверка попадания по кораблю"""
        if obj.pole[i][j] == '*':  # попадание
            self.count_hit += 1
            obj.pole[i][j] = self.count_hit  # отобразим на экране попадание
            if self.count_hit == 1:  # если первое попадание
                self.ship = self.find_ship(i, j, obj)  # получаем корабль по координатам выстрела
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                self.index_i, self.index_j = i, j  # обозначим координаты первого попадания
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    obj.ships_pole.remove(self.ship)  # удалим корабль из списка
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                    if self.count_ships:  # проверим есть ли еще корабли на поле
                        self.set_min_len_ship(obj)  # переопределим длину минимального корабля из оставшихся
                    self.ship = None  # корабль уничтожен

            elif self.count_hit == 2:  # второе попадание
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    obj.ships_pole.remove(self.ship)  # удалим корабль из списка
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                    if self.count_ships:  # проверим есть ли еще корабли на поле
                        self.set_min_len_ship(obj)  # переопределим длину минимального корабля из оставшихся
                    self.ship = None  # корабль уничтожен
                else:
                    self.determine_position_ship(self.index_i, self.index_j, i, j)  # определим позицию корабля
                    self.set_list_shots(obj)  # создаем два списка /
                    # координат обстрела относительно положения корабля

            else:
                self.ship.counter -= 1  # уменьшаем очки прочности корабля
                if self.ship.counter == 0:  # все палубы корабля подбиты
                    self.add_around_ship_index(self.ship)  # добавим координаты вокруг корабля куда стрелять не нужно
                    self.index_i, self.index_j = None, None  # индексы первого попадания больше не нужны
                    obj.ships_pole.remove(self.ship)  # удалим корабль из списка
                    self.count_ships -= 1  # уменьшаем счетчик кораблей
                    self.count_hit = 0  # обнуляем счетчик попаданий по кораблю
                    self.positive_indexes.clear()  # очистим позитивный список
                    self.negative_indexes.clear()  # очистим негативный список
                    if self.count_ships:  # проверим есть ли еще корабли на поле
                        self.set_min_len_ship(obj)  # переопределим длину минимального корабля из оставшихся
                    self.ship = None  # корабль уничтожен
        else:
            obj.pole[i][j] = '#'  # обозначим промах на поле
            if self.count_hit > 1:  # проверим, что идет добивание по координатам из позитивного списка
                self.positive_indexes.clear()  # если промах по координатам позитивного списка, очистим его /
                # (он больше не нужен)


class Player:
    """Класс игрока"""
    def __init__(self, obj, name='Player'):
        """Инициализируем данные игрока"""
        self.name = name
        self.coords_shots = {key: [] for key in range(10)}  # словарь хранения координат куда будут произведены выстрелы
        self.count_ships = len(obj.ships_pole)  # количество кораблей на поле

    def set_coords(self):
        """Ввод координат выстрела игроком"""
        print('Введите координату "i" и "j" без пробела в диапазоне от 0 до 9')
        while True:
            try:
                i, j = map(int, input())
                if not self.check_coords(i, j):
                    self.coords_shots[i].append(j)
                    return i, j
                else:
                    print('Уже стреляли по этим координатам, введите еще раз')
            except ValueError:
                print('Некорректные координаты')
                print('Введите координату "i" и "j" без пробела в диапазоне от 0 до 9')

    def check_coords(self, i, j):
        """Проверка повторения координат перед выстрелом"""
        return j in self.coords_shots[i]

    @staticmethod
    def find_ship(i, j, obj):
        """Поиск корабля по координатам попадания"""
        for ship in obj.ships_pole:  # перебираем корабли
            if any(filter(lambda x: x == (i, j), ship.cell)):  # ищем корабль, которому принадлежит координата:
                return ship

    def check_hit(self, i, j, obj):
        """Проверка попадания по кораблю"""
        if obj.pole[i][j] == '*':  # если есть попадание
            ship = self.find_ship(i, j, obj)  # найдем корабль
            ship.hits += 1  # счетчик попадания по кораблю увеличим
            ship.counter -= 1  # прочность корабля уменьшим
            obj.pole[i][j] = ship.hits  # отобразим попадание
            if ship.counter == 0:
                obj.ships_pole.remove(ship)  # удалим корабль из списка
                self.count_ships -= 1  # уменьшим счетчик оставшихся кораблей
            return ship.counter  # вернем прочность корабля
        else:
            obj.pole[i][j] = '#'  # отображение промаха


class DrawPole:
    """Класс рисования игрового поля игрока и бота"""
    def __init__(self, pole1, pole2, obj1, obj2):
        self.pole_bot = pole1  # поле бота
        self.pole_player = pole2  # поле игрока
        self.player_bot = obj1  # объект бот
        self.player = obj2  # объект игрок
        self.event_bot = None
        self.event_player = None
        self.shot = 'выстрелил'
        self.win = 'Выиграл!!!'
        self.wound = 'Ранил'
        self.mishit = 'Мимо'
        self.kill = 'Убил'
        self.indent = 10
        self.len_pole = len(pole_bot.pole)  # длина поля
        self.numer = ' '.join([str(i) for i in range(self.len_pole)])  # нумерация колонок поля
        self.draw_bot = [['.' for y in range(self.len_pole)] for x in range(self.len_pole)]  # заполнение поля бота
        self.draw_player = [['.' for y in range(self.len_pole)] for x in range(self.len_pole)]  # заполнение поля игрока

    def draw_pole(self, i1, j1, i2, j2, ship_count):
        """Рисование игровых полей"""
        self.event_bot = self.event_player = self.mishit
        self.draw_bot[i1][j1] = self.pole_bot.pole[i1][j1]
        self.draw_player[i2][j2] = self.pole_player.pole[i2][j2]
        print(f'{self.player_bot.name} {self.shot} {i1, j1}{self.player.name.rjust(19)} {self.shot} {i2, j2}')
        message_player = f'Кораблей {self.player.name} = {str(self.player_bot.count_ships).rjust(2, '0')} шт.'
        message_bot = f'Кораблей {self.player_bot.name} = {str(self.player.count_ships).rjust(2, '0')} шт.'
        print(f'{message_bot}{message_player.rjust(36)}')
        if self.draw_bot[i1][j1] in range(1, 5):
            if self.player_bot.ship:
                self.event_bot = self.wound
            else:
                self.event_bot = self.kill
        if ship_count is not None:
            if ship_count == 0:
                self.event_player = self.kill
            else:
                self.event_player = self.wound
        print(self.event_bot.ljust(32), self.event_player)
        print('  ' + self.numer, ' ' * 12, self.numer)
        for c in range(self.len_pole):
            print(c, *self.draw_bot[c], ' '*10, c, *self.draw_player[c])

    def print_win(self, obj):
        """Объявление победителя"""
        print(f'{obj.name} {self.win}')

    def finish_draw(self):
        self.draw_bot = [['*' if self.pole_bot.pole[i][j] == '*' else self.pole_bot.pole[i][j] for j in range(self.len_pole)] for i in range(self.len_pole)]
        self.draw_player = [['*' if self.pole_player.pole[i][j] == '*' else self.pole_player.pole[i][j] for j in range(self.len_pole)] for i in range(self.len_pole)]


for x in range(1):
    pole_bot = init_pole.Pole()  # инициализация поля игры для бота
    pole_player = init_pole.Pole()  # инициализация поля игры для игрока
    pole_bot.arrangement()  # расстановка кораблей на поле игрока
    pole_player.arrangement()  # расстановка кораблей на поле бота
    bot = Bot(pole_bot)  # инициализация бота
    player = Player(pole_player)
    draw = DrawPole(pole_bot, pole_player, bot, player)
    PLAY = True
    while PLAY:
        i1, j1 = bot.set_shot_coords()  # получение координаты выстрела бота
        bot.check_hit(i1, j1, pole_bot)  # проверка попадания по кораблю ботом
        i2, j2 = player.set_coords()  # игрок вводит координаты выстрела
        ship_count = player.check_hit(i2, j2, pole_player)  # проверка попадания по кораблю игроком
        draw.draw_pole(i1, j1, i2, j2, ship_count)  # вывод игровых полей на экран
        if not pole_player.ships_pole:  # проверка оставшихся кораблей у бота
            draw.print_win(player)
            PLAY = False
        if not pole_bot.ships_pole:  # проверка оставшихся кораблей у бота
            draw.print_win(bot)
            PLAY = False
    draw.finish_draw()
    for i in range(draw.len_pole):
        print(' ', *draw.draw_bot[i], '           ', *draw.draw_player[i])
