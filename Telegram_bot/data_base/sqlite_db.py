import sqlite3 as sq
from bot_create import bot


def sql_start():
    global base, cur
    # инициализация БД, если такая БД существует, то произойдет подключение к ней
    base = sq.connect('pizza_cool.db')
    # часть базы данных, которая осуществляет поиск, выборку, встраивание из БД
    cur = base.cursor()
    # этот if пропишет сообщение в консоли, если подключение к БД прошло успешно
    if base:
        print('Data base connected!')
    # Создаем таблицу, в которую будем вносить данные (текст у картинки так как она сохраняется
    # на сервере телеграмма и обращаться к ней будем по id)
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description '
                 'TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        # подстановка значений словаря (словарь формируется при добавлении в меню) в нашу БД
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# Создание меню посредством чтения БД
async def sql_read(message):
    # Выбираем все из таблицы "menu". .fetchall() выгружает данные в виде списка
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: '
                                                           f'{ret[2]}\nЦена: {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    # в переменную data передается название пиццы, затем происходит поиск и удаление пиццы
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
