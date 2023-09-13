from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки клавиатуры админа

button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete)

