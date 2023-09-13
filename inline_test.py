from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot('5932432243:AAG9plc0lLqxepPXjoP81UwUOk4Tibonteg')
dp = Dispatcher(bot)

# словарь для подсчета результатов голосования
count_dict = dict()

# Создание inline кнопок

# Клавиатура. row_width - количество кнопок в ряду
url_kb = InlineKeyboardMarkup(row_width=2)
# Кнопки. Здесь по сути мы маскируем ссылку под какую-либо надпись
url_button = InlineKeyboardButton(text='Ссылка', url='https://youtube.com')
url_button2 = InlineKeyboardButton(text='Ссылка 2', url='https://google.com')
x = [InlineKeyboardButton(text='Ссылка 3', url='https://google.com'),
     InlineKeyboardButton(text='Ссылка 4', url='https://google.com'),
     InlineKeyboardButton(text='Ссылка 5', url='https://google.com')]
# Группировка кнопок. Ограничение на количество кнопок на .row() не работает
url_kb.add(url_button, url_button2).row(*x)


# Запрос на вызов кнопок при срабатывании определенной команды
@dp.message_handler(commands='links')
async def url_command(message: types.Message):
    await message.answer('Ссылочки:', reply_markup=url_kb)


# Call_back кнопки

# В callback_data мы передаем название события, которое будем в дальнейшем обрабатывать
in_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Нажми меня',
                                                                   callback_data='www'))


@dp.message_handler(commands='test')
async def url_command(message: types.Message):
    await message.answer('Инлайн кнопка', reply_markup=in_kb)


# Улавливание события callback_data
@dp.callback_query_handler(text='www')
async def www_call(callback: types.CallbackQuery):
    # .answer выведет ответ в виде всплывающего сообщения по центру экрана
    # если изменить на .message.answer, то бот ответит тебе сообщением
    await callback.message.answer('Нажата инлайн кнопка')

    # по умолчанию бот ожидает от нас подтверждения об исполнении кода в callback_query_handler
    # (часики около кнопки крутятся ~ 20 сек), чтобы их убрать (написанное в скобках у этого
    # запроса выведется в качестве всплывающего сообщения):
    await callback.answer()

    # если к предыдущему запросу в скобки передать сообщение и параметр show_alert = True,
    # то сообщение выведется как всплывающее ОКНО, в которое помещается 200 символов


# Один handler может обрабатывать несколько inline кнопок
in_kb1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Python',
                                                                    callback_data='like_1'),
                                               InlineKeyboardButton(text='JS',
                                                                    callback_data='like_-1'))


@dp.message_handler(commands='vote')
async def voting(message: types.Message):
    await message.answer('Какой язык лучше?', reply_markup=in_kb1)


# обработка голосования при помощи встроенного модуля Text
@dp.callback_query_handler(Text(startswith='like_'))
async def voting_call(cb: types.CallbackQuery):
    # отбрасываем ненужную при обработке часть при помощи text.split
    result = int(cb.data.split('_')[1])
    if cb.from_user.id not in count_dict:
        count_dict[cb.from_user.id] = result
        await cb.answer('Вы проголосовали')
    else:
        await cb.answer('Вы уже проголосовали', show_alert=True)


executor.start_polling(dp, skip_updates=True)
