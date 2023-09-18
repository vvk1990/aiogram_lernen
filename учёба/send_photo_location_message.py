from aiogram import Bot, Dispatcher, executor, types

TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

HELP = '''
/<b>help</b> -<em>сыписок команд</em>
/<b>start</b> - <em>начать работу с ботом</em>
/<b>photo</b> - <em>откроется фото</em>
/<b>location</b> - <em>локация</em>'''



async def on_startup(_):
    print('Погнали!)')

# создаем обработчик сообщения /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(HELP, parse_mode="HTML")


# использование мода(parse_mode="HTML") для изменения текста с помощью примочек
@dp.message_handler(commands=['start'])
async def start_command(massage: types.Message):
    await massage.answer('<em>привет  <b>тестим</b> хтмл разметку</em>', parse_mode="HTML")


# send_photo
@dp.message_handler(commands=['photo'])
async def help_command(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id, photo='https://ae04.alicdn.com/kf/H01fec09dd92143bbbd8eb7404a1c202cb.jpg')
    await message.delete()# удалим сообщение пользователя из общего чата

# send_location
@dp.message_handler(commands=['location'])
async def send(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            longitude=55,
                            latitude=74)
    await message.delete()# удалим сообщение пользователя из общего чата
    
# send_message
@dp.message_handler()
async def help_command(message: types.Message):
    # await message.answer(message.text)
    # await bot.send_message(chat_id=message.chat.id, text='hallo')# отправляет hallo в чат общий
    # await bot.send_message(chat_id=message.from_user.id, text='hallo')# отправляет hallo в чат личный
    await bot.send_message(chat_id=message.from_user.id, text=HELP, parse_mode="HTML")# отправим в личку команды
    await message.delete()# удалим сообщение пользователя из общего чата



executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
#skip_updates=True - для того чтобы бот не отвечал на сообщения отправленные в оффлайне бота