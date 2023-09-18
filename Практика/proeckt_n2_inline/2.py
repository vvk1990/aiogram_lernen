import uuid

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN_API
from aiogram.utils.callback_data import CallbackData

import hashlib

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

# cb = CallbackData('ikb', 'action')
bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

user_data = ''

async def on_startup(_):
    print('Погнали!)')

@dp.message_handler(commands=['start'])
async def cdm_start(message: types.Message):
    await message.answer('Приветики')


@dp.message_handler()
async def cdm_start(message: types.Message):
    global user_data
    user_data = message.text
    await message.answer('save')


@dp.inline_handler()
async def inline_article(inline_query: types.InlineQuery):
    text = inline_query.query or 'Empty'
    input_content_bold = types.InputTextMessageContent(f'<b>{text}</b>',
                                            parse_mode='html')
    input_content_italica = types.InputTextMessageContent(f'_{text}_',
                                                 parse_mode='html')

    item_1 = types.InlineQueryResultArticle(
        input_message_content=input_content_bold,
        id=str(uuid.uuid4()),
        title='Bold',
        description=text,
        thumb_url='https://www.turunculevye.com/wp-content/uploads/2022/10/eFootball-2023-Dostluk-Maci-ve-Fazlasina-Kavustu.jpg'
    )

    item_2 = (
        input_message_content=in,
        id=str(uuid.uuid4()),
        title='Italic',
        description=text,
        thumb_url='https://www.turunculevye.com/wp-content/uploads/2022/10/eFootball-2023-Dostluk-Maci-ve-Fazlasina-Kavustu.jpg'
    )

    await bot.answer_inline_query(results=[item],
                                  inline_query_id=inline_query.id,
                                  cache_time=1)

executor.start_polling(skip_updates=True,
                           dispatcher=dp,
                           on_startup=on_startup)