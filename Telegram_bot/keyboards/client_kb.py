# Класс KeyboardButton позволяет нам создавать кнопки
# Класс ReplyKeyboardMarkup замещает обычную клавиатуру той, что мы создаем

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
button1 = KeyboardButton('/working_time')
button2 = KeyboardButton('/address')
button3 = KeyboardButton('/menu')

# button4, button5 - Кнопки запроса телефона и локации
# button4 = KeyboardButton('give number', request_contact=True)
# button5 = KeyboardButton('give location', request_location=True)

# resize_keyboard - подгоняет кнопки под размер устройства
# one_time_keyboard - показывает клавиатуру только один раз
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

# Методы добавления кнопок:
#   1. add - кнопка добавится на всю строку
#   2. insert - кнопка попытается влезть в текущую строку, если не получится - добавится в след.
#   3. row - сюда можно передать несколько кнопок для создания строки из кнопок

kb_client.add(button1).add(button2).add(button3)
# kb_client.row(button4, button5)

