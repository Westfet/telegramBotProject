# executor нужен для запуска бота
from aiogram.utils import executor

from bot_create import dp

from handlers import client, admin, other

from data_base import sqlite_db


# # Aiogram - асинхронная библиотека, это значит, что бот, работая в однопоточном режиме, будет
# # лучше справляться с нагрузкой от пользователей. Функции в библиотеке асинхронные (async)
# async def echo_send(message: types.Message):
#     # await в асинхронной функции означает "подождать", пока освободится время на выполнение

# !!! Способы отправки сообщений
#     # 1. простой ответ на сообщение
#     await message.answer(message.text)
#     # 2. ответ с указанием сообщения, на которое отвечает бот
#     # await message.reply(message.text)
#     # 3. ответ в личные сообщения, если сообщение пользователя написано в какой-то группе
#     # await bot.send_message(message.from_user.id, message.text)

# !!! Способы парсинга сообщений от пользователя (например пользователь не знает, с помощью какой
# команды в боте можно заказать такси и просто пишет "заказать такси")
# Для парсинга вместо "in" можно также использовать startwith или endwith
# @dp.message_handler(lambda message: 'такси' in message.text)
# async def taxi(message):
#     await message.answer('Чтобы заказать такси...')


# функция, запускающаяся при bot pooling (обязательно добавить в execute)
async def on_startup(_):
    print('Бот вышел в онлайн')
    # запуск БД при запуске бота
    sqlite_db.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

# если не записать команду skip_updates, то бот при запуске начнет отвечать на сообщения,
# написанные в момент, когда бот был не активен
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
