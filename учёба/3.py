from aiogram import Bot, Dispatcher, executor, types

TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

HELP_COMMAND = ''' 
/<b>help</b> -<em>сыписок команд</em>
/<b>start</b> - <em>начать работу с ботом</em>
/<b>give</b> - <em>на команду /give отправляем в личку юзеру(massage.from_user.id) стикер с  канала  в телеге Get Sticker ID</em>
'''

async def on_startup(_):
    print('Погнали!)')

kol_v = 0

# создаем обработчик сообщения /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(HELP_COMMAND, parse_mode="HTML")


# использование мода(parse_mode="HTML") для изменения текста с помощью примочек
@dp.message_handler(commands=['start'])
async def start_command(massage: types.Message):
    await massage.answer('<em>привет  <b>тестим</b> хтмл разметку</em>', parse_mode="HTML")

# создаем обработчик сообщения /give
@dp.message_handler(commands=['give'])
async def start_command(massage: types.Message):
    '''на команду /give отправляем в личку юзеру(massage.from_user.id) стикер с  канала  в телеге Get Sticker ID'''
    await bot.send_sticker(massage.from_user.id, sticker='CAACAgIAAxkBAAEJAxxkZPkxWBZv0ELq_31QGoQglN0P4gACBQADwDZPE_lqX5qCa011LwQ')
    await massage.delete()

# # создаем обработчик сообщения и поиск и подсчет символа(v)
# @dp.message_handler()
# async def help_command(message: types.Message):
#     global kol_v
#     for simvol in message.text:
#         if simvol == 'v':
#             kol_v += 1
#     await message.answer(f'kol v = {kol_v}, {message.text}')

# создаем обработчик сообщения и поиск и подсчет символа и тд
@dp.message_handler()
async def help_command(message: types.Message):
    global kol_v
    for simvol in message.text:
        if simvol == '😋':
            print('ch')

        elif simvol == 'b':
            kol_v += 1
            await message.answer('🙊')

        elif simvol == 'v':
            kol_v += 1
            await message.answer(f'kol v = {kol_v}, {message.text}')

    await message.answer('🌚')

# создаем обработчик сообщения отправляем стикер

# стикеры. в ответ на стикер бот отправляет id стикера и стикер под id там прописан
@dp.message_handler(content_types=['sticker'])
async def send_sticker_id(message: types.Message):
    await message.answer(message.sticker.file_id)
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAOpZGYtDN7fDAv_AwZUPIslpoZKX0AAAhEAA8A2TxMNqrMP3B4-5S8E')

executor.start_polling(dp, on_startup=on_startup)