# Bot - класс для создания ботов
from aiogram import Bot

# Dispatcher - улавливатель событий
from aiogram.dispatcher import Dispatcher

# os нужно, чтобы прочитать токен с bat файла
import os

# MemoryStorage - класс, позволяющий хранить данные в оперативной памяти. Это необходимо,
# чтобы запомнить данные от пользователя и перенаправить их куда-то, например в БД
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)
