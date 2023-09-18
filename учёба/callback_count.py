from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера


number = 0
def get_iline_keyboard()->InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('+', callback_data='btn_inkrease'),
         InlineKeyboardButton('-', callback_data='btn_dislike')],
    ])

    return ikb

@dp.message_handler(commands=['start'])
async def cdm_start(message: types.Message):
    await message.answer(f'klassick {number}',
                         reply_markup=get_iline_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))# фильтруем сообщения и реагируем на сообзения начинабщиеся на 'btn'
async def ikb_cd_handler(callbeck: types.CallbackQuery):
    global number
    if callbeck.data == 'btn_inkrease':
        number += 1
        await callbeck.message.edit_text(f'klassick {number}',
                                         reply_markup=get_iline_keyboard())
    elif callbeck.data == 'btn_dislike':
        number -= 1
        await callbeck.message.edit_text(f'klassick {number}',
                                         reply_markup=get_iline_keyboard())

async def on_startup(_):
    print('Погнали!)')



executor.start_polling(skip_updates=True,
                           dispatcher=dp,
                           on_startup=on_startup)