from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота
import random
from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера


kb = ReplyKeyboardMarkup(resize_keyboard=True)
                         #)# создали клавиатуру,
# вписывающейся в интерфейс(resize_keyboard=True),
# и самозакрывается (one_time_keyboard=True)

kb.add(KeyboardButton('/help'))# cоздали кнопку
kb.insert(KeyboardButton('/discription'))
kb.add(KeyboardButton('/herz'))
kb.add(KeyboardButton('/location'))
HELP = '''
/<b>help</b> -<em>сыписок команд</em>
/<b>start</b> - <em>начать работу с ботом</em>
/<b>discription</b> - <em>начать работу с ботом</em>
/<b>herz</b> - <em>отправится сердце</em>
/<b>location</b> - <em>локация</em>'''

async def on_startup(_):
    print('Погнали!)')

# send_location
@dp.message_handler(commands=['location'])
async def send_randim(message: types.Message):
    x = random.randint(1, 100)
    y = random.randint(1, 100)
    await bot.send_location(chat_id=message.chat.id,
                            longitude=x,
                            latitude=y)
    await message.delete()# удалим сообщение пользователя из общего чата

# создаем обработчик сообщения /help(отправляем в личку)
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP,
                           parse_mode="HTML",
                           reply_markup=kb
                           )
    await message.delete()

@dp.message_handler(commands=['start'])
async def start_command(massage: types.Message):
    await bot.send_message(chat_id=massage.chat.id,
                           text='Добропожаловать',
                           parse_mode="HTML",
                           reply_markup=kb)

# создаем обработчик сообщения /help(отправляем в личку)
@dp.message_handler(commands=['discription'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Упражняемся с кнопками',
                           parse_mode="HTML",
                           reply_markup=ReplyKeyboardRemove(),# клавиатура закрывается после наж.
                           )
    await message.delete()

@dp.message_handler(commands=['herz'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='❤️',
                           parse_mode="HTML",
                           )
    await message.delete()


executor.start_polling(dp, on_startup=on_startup, skip_updates=True)