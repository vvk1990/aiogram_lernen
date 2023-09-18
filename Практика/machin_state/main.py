# изучаем машиносостояние

from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import  FSMContext

from config import TOKEN_API



storage = MemoryStorage()
bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot,
                storage=storage) # создали диспетчера


async def on_startup(_):
    print('Погнали!)')


def get_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Начать работу!'))

    return kb

def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

class ClientStartesGroup(StatesGroup):

    photo = State()
    desc = State()


@dp.message_handler(commands=['start'])
async def cdm_start(message: types.Message):
    await message.answer('Приветики',
                         reply_markup=get_keyboard())

@dp.message_handler(commands=['cancel'], state='*')
async def start_work(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('отменил',
                        reply_markup=get_keyboard())
    await state.finish()

@dp.message_handler(Text(equals='Начать работу!', ignore_case=True ), state=None)
async def start_work(message: types.Message):
    await ClientStartesGroup.photo.set()
    await message.answer('отравь фото',
                         reply_markup=get_cancel())


@dp.message_handler(lambda message: not message.photo, state=ClientStartesGroup.photo)
async def check_photo(message: types.Message):
    return await message.reply('это не фото')


@dp.message_handler(lambda message: message.photo,content_types=['photo'], state=ClientStartesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await ClientStartesGroup.next()
    await message.reply('А теперь отрпавь нат описание!')

@dp.message_handler( state=ClientStartesGroup.desc)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text

    await message.reply('Ваша фотограыия сохранена!')

    async with state.proxy() as data:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=data['desc'])


@dp.message_handler(commands=['cancel'], state='*')
async def start_work(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('отменил')
    await state.finish()


executor.start_polling(skip_updates=True,
                           dispatcher=dp,
                           on_startup=on_startup)