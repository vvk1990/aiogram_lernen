from aiogram import Bot, Dispatcher, executor, types

TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

async def on_startup(_):
    print('Бот был успешно запущен')


# использование мода(parse_mode="HTML") для изменения текста с помощью примочек
@dp.message_handler(commands=['start'])
async def start_command(massage: types.Message):
    await massage.answer('<em>привет  <b>тестим</b> хтмл разметку</em>', parse_mode="HTML")

# стикеры
@dp.message_handler(commands=['give'])
async def start_command(massage: types.Message):
    '''на команду /give отправляем в личку юзеру(massage.from_user.id) стикер с  канала  в телеге Get Sticker ID'''
    await bot.send_sticker(massage.from_user.id, sticker='CAACAgIAAxkBAAEJAxxkZPkxWBZv0ELq_31QGoQglN0P4gACBQADwDZPE_lqX5qCa011LwQ')
    await massage.delete()
# эмоджи
@dp.message_handler()
async def start_command(massage: types.Message):
    '''на команду /give отправляем в личку юзеру(massage.from_user.id) стикер с  канала  в телеге Get Sticker ID'''
    await  massage.answer(f'{massage.text}, 😃')
    await massage.delete()






executor.start_polling(dp, on_startup=on_startup)