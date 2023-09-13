# Этот импорт нужен, чтобы указывать, что handler используется в конкретном месте
from aiogram.dispatcher import FSMContext

from bot_create import dp, bot

from aiogram.dispatcher.filters import Text

# импорт классов состояний
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram import types, Dispatcher
from data_base import sqlite_db
from keyboards import admin_kb

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ************************************ЗАГРУЗКА ДАННЫХ В МЕНЮ*************************************

# Класс для организации добавления новой позиции в меню
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


ID = None


# Получаем ID текущего администратора. Проверка на то, что это действительно админ - внизу в
# регистрируемых handler's для этой функции is_chat_admin = True
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Привет, администратор !',
                           reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Начало диалога загрузки пункта в меню. Так как это handler старта, бот не находится ни в каком
# состоянии, поэтому state=None

async def cm_start(message: types.Message):
    # проверка пользователя на модератора
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


# Выход из состояния
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ок')


# Отлавливаем первый ответ и записываем его в словарь временного хранилища. При помощи state=
# FSMAdmin.photo вводим бота в цепочку состояний в пункт photo
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        # Сохраняем картинку в словарь с помощью контекстного менеджера with
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            # Ожидание следующего состояния из цепочки
            await FSMAdmin.next()
            await message.reply('Теперь введи название')


# Отлавливаем второй ответ от администратора. По аналогии с загрузкой фото
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введи описание')


# Отлавливаем третий ответ от администратора. По аналогии с загрузкой фото
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь Введи цену')


# Отлавливаем четвертый ответ от администратора. По аналогии с загрузкой фото
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        # при исп. команды state.finish бот выходит из машины состояний и полностью очищает словарь
        await state.finish()


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        # Чтение базы данных и запись их в переменную read
        read = await sqlite_db.sql_read2()
        for i in read:
            # Отправляем админу описание всех пицц
            await bot.send_photo(message.from_user.id, i[0], f'{i[1]}\nЦена {i[-1]}')
            # Добавляем тематические стрелочки для наглядности + кнопку 'delete'
            await bot.send_message(message.from_user.id, text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                       # в callback_data сохраняем название пиццы,
                                       # которое будем отправлять в БД
                                       f'delete {i[1]}', callback_data=f'del {i[1]}')))


# callback отработает только в том случае, если в переменной находятся какие-то данные и эти
# данные начинаются с 'del '
# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    # выполняем удаление пиццы
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    # уведомляем telegram о том, что запрос выполнен, параллельно с этим выводим всплывающее
    # сообщение для администратора
    await callback_query.answer(text=f'{callback_query.data.replace("del ", " ")} удалена.',
                                show_alert=True)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, content_types=['text'], state=FSMAdmin.name)
    dp.register_message_handler(load_description, content_types=['text'],
                                state=FSMAdmin.description)
    dp.register_message_handler(load_price, content_types=['text'], state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(delete_item, commands='Удалить', state=None)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
