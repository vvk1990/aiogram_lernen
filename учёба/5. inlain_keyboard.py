from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота
import random
from config import TOKEN_API
from in_key import ikb

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

HELP = '''
/<b>help</b> -<em>сыписок команд</em>
/<b>start</b> - <em>начать работу с ботом</em>
/<b>links</b> - <em>начать работу с ботом</em>
'''

# создали инлайн клавиатуру

# ikb = InlineKeyboardMarkup(row_width=2)
# bat1 = InlineKeyboardButton(text='Button 1',
#                             url='https://www.youtube.com/watch?v=qivjEiONPy4'
#                             )
# bat2 = InlineKeyboardButton(text='Button 2',
#                             url='https://www.youtube.com/watch?v=qivjEiONPy4')
#
# ikb.add(bat1)
# ikb.insert(bat2)

# создали клавиатуру
kb = ReplyKeyboardMarkup(resize_keyboard=True)
                         #)# создали клавиатуру,
# вписывающейся в интерфейс(resize_keyboard=True),
# и самозакрывается (one_time_keyboard=True)

kb.add(KeyboardButton('/links'))# cоздали кнопку
kb.add(KeyboardButton('/help'))

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP,
                           parse_mode="HTML",
                           )
    await message.delete()

@dp.message_handler(commands=['links'])
async def start_command(massage: types.Message):
    await bot.send_message(chat_id=massage.chat.id,
                           text='hallo',
                           reply_markup=ikb)

@dp.message_handler(commands=['start'])
async def start_command(massage: types.Message):
    await bot.send_message(chat_id=massage.chat.id,
                           text='Добро пожаловать',
                           reply_markup=kb)

async def on_startup(_):
    print('Я был запущен!)')


executor.start_polling(dp, on_startup=on_startup, skip_updates=True)