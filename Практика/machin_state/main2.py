# изучаем машиносостояние, создаём разные состаяния для бота

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

# from aiogram.dispatcher.filters import Text

from config import TOKEN_API
from

storage = MemoryStorage()
bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot, storage=storage) # создали диспетчера


async def on_startup(_):
    print('Погнали!)')

class ProfileStatesGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()



def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    return kb

def get_cancel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb
#
@dp.message_handler(commands=['cancel'], state='*')# если нажали cancel в любом из состаяний
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state  == None:
        return

    await state.finish()
    await message.reply('Вы пресрвалм создание анкеты!',
                        reply_markup=get_kb())

@dp.message_handler(commands=['start'])
async def cdm_start(message: types.Message):
    await message.answer('Привет нажми  type / create',
                         reply_markup=get_kb())



@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message):
    await message.reply('Для начала добавьте фото',
                        reply_markup=get_cancel())
    await ProfileStatesGroup.photo.set()# настраеваем бота на ожидание фотографии

    # async def set(self: state):
    #     state = Dispatcher.get_current().current_state()
    #     await state.set_state(self.state)

# этот хендлер решает, если это не фото тогда пишет сообщение об этом
@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo)# если это не фото то...
async  def check_photo(message: types.Message):
    await message.reply('Это не фотография!')

@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo)# обрабатывает фото если у ниго состаяние фото
async def load_photo(message: types.Message, state: FSMContext ):
    async with state.proxy() as data: # используем with чтобы открвть хранилище для данных
        data['photo'] = message.photo[0].file_id # сохраняем id фото в славаре под ключём 'photo'

    await message.reply('Теперь отправь своё имя!')
    await ProfileStatesGroup.next()# переключаем бота в следующее состаяние

@dp.message_handler(state=ProfileStatesGroup.name)# обрабатывает  состаяние name
async def load_name(message: types.Message, state: FSMContext ):
    async with state.proxy() as data:
        data['name'] = message.text  # сохраняем имя введеное пользователем в славаре под ключём 'name'

    await message.reply('Теперь отправь свой возраст!')
    await ProfileStatesGroup.next()

# этот хендлер решает, если это не цыфра тогда пишет сообщение об этом
@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) > 100, state=ProfileStatesGroup.photo)# если это не число и бльше 100...
async  def check_photo(message: types.Message):
    await message.reply('Это не число!')


@dp.message_handler(state=ProfileStatesGroup.age)# обрабатывает  состаяние age
async def load_age(message: types.Message, state: FSMContext ):
    async with state.proxy() as data:
        data['age'] = message.text  # сохраняем возрост введеное пользователем в славаре под ключём 'age'

    await message.reply('Раскажи немного о себе!')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.description)# обрабатывает состаяние description
async def load_disceiption(message: types.Message, state: FSMContext ):
    async with state.proxy() as data:
        data['description'] = message.text  # сохраняем имя введеное пользователем в славаре под ключём 'name'
        await  bot.send_photo(chat_id=message.from_user.id,
                              photo=data['photo'],
                              caption=f"{data['photo']}, {data['age']}, {data['description']}"
                              )
    await message.reply('Ваша анкнта успешно создана')
    await state.finish() # завершаем состаяние




executor.start_polling(skip_updates=True,
                           dispatcher=dp,
                           on_startup=on_startup)