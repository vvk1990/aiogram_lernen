from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove

from aiogram.dispatcher.filters import Text

from config import TOKEN_API
from in_keyboard import kb, ikb, kb2

import random

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP = '''
/<b>help</b> -<em>сыписок команд</em>
/<b>start</b> - <em>начать работу с ботом</em>
/<b>links</b> - <em>начать работу с ботом</em>
/<b>description</b> - <em>начать работу с ботом</em>
'''
PHOTO = [
         'https://upload.wikimedia.org/wikipedia/ru/thumb/1/11/The_Lost_City_%282022%29.jpg/800px-The_Lost_City_%282022%29.jpg',
        'https://msk-apple.ru/image/cache/catalog/Add/13%20mini/30059018bb-700x700.jpg',
        'https://msk-apple.ru/image/cache/catalog/Add/13%20pro%20max/30059051bb-700x700.jpg'
        ]

photos = dict(zip(PHOTO, ['1', '2', '3']))

flag = True
flag2 = True

async def on_startup(_):
    print('Погнали!)')


async def send_random(message: types.Message):
    random_photo = random.choice(list(photos.keys()))
    await bot.send_photo(chat_id=message.chat.id,
                         photo=random_photo,
                         caption=photos[random_photo],
                         reply_markup=ikb)

# эти два хендлера ловят сообщения после нажатия кнопок и реагируют на них
@dp.message_handler(Text(equals='Random photo'))
async def open_kb_photo(message: types.Message):
    await message.answer(text='нажми на кнопку рандом',
                         reply_markup=ReplyKeyboardRemove())
    await send_random(message)
    await message.delete()


@dp.message_handler(Text(equals='Menu'))
async def open_kb_photo(message: types.Message):
    await message.answer(text='добро пожаловать в главное меню',
                         reply_markup=kb)
    await message.delete()
#____________________________________________________________________
# хендлеры реагируюшие на команды
@dp.message_handler(commands=['start'])
async def start_command(messge: types.Message):
    await bot.send_message(chat_id=messge.chat.id,
                           text='Приветстую вас главном меню!',
                           reply_markup=kb)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP,
                           parse_mode="HTML",
                           )
    await message.delete()


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP,
                           parse_mode="HTML",
                           reply_markup=ReplyKeyboardRemove()  # клавиатура закрывается после наж.
                           )
    await message.delete()

@dp.callback_query_handler()
async def random_photo_callback(callback: types.CallbackQuery):
    global flag
    global flag2
    if callback.data == 'like':
        if flag == False:
            await callback.answer('Ты уже сделал этот выбор')
        else:
            await callback.answer('Тебе понравилась эта фотография')
            flag = False
    elif callback.data == 'dislike':
        if flag2 == False:
            await callback.answer('Тебе не понравилась эиа фотография')
            flag2 = False
        else:
            await callback.answer('Ты уже сделал этот выбор')
    else:
        # рандомно возмем из словаря фото(ключом) с данными
        random_photo = random.choice(list(photos.keys()))
        # когда ползователь нажимает кнопку 'Следующее фото', фото заменяется другим и запускается клава ikb
        await callback.message.edit_media(types.InputMedia(media=random_photo,
                                                           types='photo',
                                                           caption=photos[random_photo]),
                                                           reply_markup=ikb
                                                           )
        print(flag, flag2)
        # await send_random(message=callback.message)
        await callback.answer()

@dp.message_handler(commands='lacation')
async def cmd_location(message: types.Message):
    await bot.send_location(chat_id=message.chat.id,
                            latitude=random.randint(50, 100),
                            longitude=random.randint(50, 100))


if __name__ == "__main__":
    executor.start_polling(skip_updates=True,
                           dispatcher=dp,
                           on_startup=on_startup)