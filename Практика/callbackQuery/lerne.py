from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота
import random
from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера


async def on_startup(_):
    print('Погнали!)')

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('like', callback_data='like'),
     InlineKeyboardButton('dislike', callback_data='dislike'),
     InlineKeyboardButton('Exit', callback_data='exit')],
])

flag = True
flag2 = True


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo='https://cdnn21.img.ria.ru/images/07e6/02/17/1774572568_0:160:3072:1888_1920x0_80_0_0_351fa68f594d0e2bc467fed10a258bbd.jpg',
                         caption='Нравится ли тебе фото?',
                         reply_markup=ikb)

@dp.callback_query_handler()
async def ikb_cb_handleer(callback: types.CallbackQuery):
    global flag
    if callback.data == 'like':
        if flag == False:
            await callback.answer('Ты уже сделал выбор',
                                  show_alert=True)
        else:
            await callback.answer('Тебе понравилась эта фотография')
            flag = False
    elif callback.data == 'dislike':
        if flag == False:
            await callback.answer('Ты уже сделал выбор',
                                  show_alert=True)
        else:
            await callback.answer('Тебе не понравилась эта фотография')
    elif callback.data == 'exit':
        await callback.message.delete()



executor.start_polling(dp, on_startup=on_startup, skip_updates=True)