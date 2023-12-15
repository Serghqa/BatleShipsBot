import bot
import init_pole

for x in range(1):
    pole_bot = init_pole.Pole()  # инициализация поля игры для бота
    pole_player = init_pole.Pole()  # инициализация поля игры для игрока
    pole_bot.arrangement()  # расстановка кораблей на поле игрока
    pole_player.arrangement()  # расстановка кораблей на поле бота
    bot = bot.Bot(pole_bot)  # инициализация бота
    player = bot.Player(pole_player)
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
