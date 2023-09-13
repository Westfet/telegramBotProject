# декораторы намеренно закомментированы - при нынешней организации файлов они не требуются

# types - типы для аннотации типов
from aiogram import types, Dispatcher
from bot_create import dp, bot
from keyboards import kb_client
# ReplyKeyboardRemove нужен для того, чтобы убрать клавиатуру после выполнения какой-либо команды
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


# обработка команд /start и /help
# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    # обработка ошибки, возникающей в том случае, если пользователь не "активировал" бота,
    # а просто написал команду в группу
    try:
        # reply_markup - меняет клавиатуру на кнопки
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \n'
                            'https://t.me/JermainTest_bot')


# Создание других команд

# @dp.message_handler(commands=['working'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пн-Пт с 9:00 до 20:00, Сб-Вс с 11:00 до 23:00')


# @dp.message_handler(commands=['address'])
async def pizza_location_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Санкт-Петербург, ул.Пушкина 15',
                           reply_markup=ReplyKeyboardRemove())


async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands='working_time')
    dp.register_message_handler(pizza_location_command, commands='address')
    dp.register_message_handler(pizza_menu_command, commands='menu')
