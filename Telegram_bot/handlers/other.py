import json
import string

from aiogram import types, Dispatcher

from bot_create import dp


# @dp.message_handler()
async def censure(message: types.Message):
    # из текста сообщения создаем множество, попутно проверяя, не стоит ли между буквами у плохих
    # слов каких-либо знаков препинания с помощью метода translate
    # далее проверяем наше сообщение(множество) на наличие плохих слов(трансформируем список с
    # плохими словами во множество) при помощи метода intersection
    # если совпадений нет, то вернется пустое множество set()
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i
        in message.text.split(' ')}.intersection((set(json.load(open('censure.json'))))) != set():
        await message.reply('Маты запрещены')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(censure)
