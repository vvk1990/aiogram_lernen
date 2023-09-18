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
async def inline_echo(inline_query: types.InlineQuery):
    text = inline_query.query or 'Echo'
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    input_content = InputTextMessageContent(f'<b>{text}</b>-{user_data  }',
                                            parse_mode='html')
    item =types.InlineQueryResultArticle(
        input_message_content=input_content,
        id=result_id,
        title='Echo bot',
        description='Привет я не простой эхо бот',

    )

    await bot.answer_inline_query(results=[item],
                                  inline_query_id=inline_query.id,
                                  cache_time=1)

executor.start_polling(skip_updates=True,
                           dispatcher=dp,
                           on_startup=on_startup)