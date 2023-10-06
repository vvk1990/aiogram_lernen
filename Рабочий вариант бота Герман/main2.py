from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import TOKEN_API
import PrintList
import sys
from PyQt5 import QtWidgets

# # машина состояний
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#
# # запускаем машину
storage = MemoryStorage()


# FSM для регистрации нового клиента
class FSMAdmin_Clients(StatesGroup):
    Name = State()
    Phone_number = State()
    Address = State()
    Name_shop = State()
    Citi = State()
    Wiring = State()
    Confirmation = State()


# FSM для изменения данных клиента
class FSMAdmin_Clients_change(StatesGroup):
    Id = State()
    Name = State()
    Phone_number = State()
    Address = State()
    Name_shop = State()
    Citi = State()
    Wiring = State()
    Confirmation = State()


# FSM для add ЗАЯВКИ
class FSMAdmin_applications_add(StatesGroup):
    Id = State()
    Confirmation = State()


# FSM для удаления ЗАЯВКИ
class FSMAdmin_applications_del(StatesGroup):
    Id = State()


# FSM для add постоянной ЗАЯВКИ
class FSMAdmin_constant_applications_add(StatesGroup):
    Id = State()
    Confirmation = State()


# FSM для del постоянной ЗАЯВКИ
class FSMAdmin_constant_applications_del(StatesGroup):
    Id = State()
    Confirmation = State()


# FSM для удаления клиента
class FSMAdmin_Clients_del(StatesGroup):
    Id = State()
    Confirmation = State()


# FSM для регистрации нового хлеба
class FSMAdmin_Brod_add(StatesGroup):
    Name = State()
    Heft = State()
    Price_jr = State()
    Price_sl = State()
    Photo = State()
    Confirmation = State()


# FSM для изменения данных хлеба
class FSMAdmin_Brod_change(StatesGroup):
    ID = State()
    Name = State()
    Heft = State()
    Price_jr = State()
    Price_sl = State()
    Photo = State()
    Confirmation = State()


# FSM для удаления данных хлеба
class FSMAdmin_Brod_del(StatesGroup):
    ID = State()
    Confirmation = State()


# моё
import keyboard
import bd

bot = Bot(TOKEN_API)  # создали бота
dp = Dispatcher(bot, storage=storage)  # создали диспетчера и запустили бота и fsm

# menu 'Заявки'- ловим id в виде числа и сохраним нё в id_and_name_clients(в конце очистим))
id_and_name_clients = []
# список для изменения заявки (в конце очистим))
id_and_name_clients2 = []
# создадим переменную с ID клиента для работы с постоянными заявками
id_clients_end_day_of_weec_permanent_applications = []

# Создадим строку с контактами
kontakts = '<b>Полное наименование организации:</b>\n' \
           '<em>Общество с ограниченной ответственностью «Колос ГмбХ»</em>\n' \
           '<b>Юридический адрес:</b>\n' \
           '<em>658839, Алтайский край, г.Яровое, квартал «В», дом 27</em>\n' \
           '<b>ИНН:</b>\n' \
           '<em>2211000860</em>\n' \
           '<b>Генеральный директор:</b>\n' \
           '<em>Кениг Владимир Владимирович</em>\n' \
           '<b>Email:</b>\n' \
           '<em>kolos.gmbh@gmail.com</em>\n' \
           '<b>Телефон (факс):</b>\n' \
           '<em>+7(913)099-54-13</em>'

# Создадим строку с Вакансиями
vacancies = '<b>В данный момент требуются:</b>\n' \
            '- Пекарь - <em>(обучение 3 месяца с з/п)</em>\n' \
            '- Тестовод - <em>(обучение 3 месяца с з/п)</em>\n' \
            '- Грузчик-водитель - <em>(обучение 2 недели с з/п)</em>\n' \
            '- Уборщица -  <em>(в магазин "Ассорти")</em>\n' \
            '<b>Подробнее можно узнать по телефрну:</b>\n' \
            '<em>+7(913)099-54-13</em>'

# Список хлеба

# зайдем в bd и выташим список хлеба
list_brod = bd.price_name()

# Поместим имена в список в нужном формате
list_name_brod_osnov = []
for brod in list_brod:
    list_name_brod_osnov.append(brod)

# list_name_brod_osnov = ['Батон "Сдобный"___________',
#                         'Батон "Французский"_______',
#                         '"Богатырский" отрубной 0,3',
#                         '"Богатырский" отрубной 0,5',
#                         'Хлеб "Дарк 8 злаков"______',
#                         'Хлеб "Классический 075"___',
#                         'Хлеб "Классический 050"___',
#                         'Хлеб "Классический 035"___',
#                         'Хлеб "Купеческий" с изюмом',
#                         'Хлеб "Купеческий" с тмином',
#                         'Хлеб "Овсяный"____________',
#                         'Хлеб "Степной"____________',
#                         'Хлеб "Тостовый"___________',
#                         'Хлеб "Чиабатта"___________',
#                         'Хлеб "Яровской" ржаной____',
#                         'Булочка "К чаю"___________',
#                         'Булочка "С корицей"_______',
#                         'Булочка С кориц. и кремом ',
#                         'Булочка "С чесноком"______',
#                         'Булочка "Гамбургер" с кунж',
#                         'Булочка "Хот_дог" сдобная_',
#                         'Булочка "Плетёнка" с маком',
#                         'Булочка "Плюшка"__________',
#                         '"Растегай c повидлом"_____',
#                         '"Рогалик"_________________',
#                         '"Рулет с маком"___________',
#                         'Тесто "Пирожковое" охлажд.',
#                         '"Пряники"_________________',
#                         '"Ватрушка" створогом______',
#                         '"Ватрушка" с сыром________',
#                         '"Ватрушка" с конфитюром___',
#                         'Беляш_печеный_____________',
#                         '"Кекс классический"_______',
#                         '"Кекс шоколадный"_________',
#                         '"Кулебяка"________________',
#                         '"Пирожок с капустой"______',
#                         '"Пирожок с яблоками"______',
#                         '"Пицца_мини"______________',
#                         '"Ромовая баба"____________',
#                         '"Сосиска в тесте"_________'
#
#
#                         ]

# зайдем в bd  и вытызим список хлеба (нужна длина списка)
list_application1 = [0] * len(bd.price_name())

# list_aplication1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                     0, 0, 0, 0, 0, 0, 0]

# списки хлеба для печати
list_name_brod2_osnov = ['Батон_Сдобный',
                         'Батон_Французский',
                         'Хлеб_Богатырский_отрубной',
                         'Хлеб_Богатырский_отрубной_круглый',
                         'Хлеб_Дарк_8_злаков',
                         'Хлеб_Классический_075',
                         'Хлеб_Классический_050',
                         'Хлеб_Классический_035',
                         'Хлеб_Купеческий_заварной_с_изюмом',
                         'Хлеб_Купеческий_заварной_с_тмином',
                         'Хлеб_Овсяный',
                         'Хлеб_Степной',
                         'Хлеб_Тостовый',
                         'Хлеб_Чиабатта',
                         'Хлеб_Яровской_ржаной',
                         'Булочка_К_чаю',
                         'Булочка_С_корицей',
                         'Булочка_С_корицей_и_кремом',
                         'Булочка_С_чесноком',
                         'Булочка_С_кунжутом_для_гамбургера',
                         'Булочка_Сдобная_для_хот_дога',
                         'Плетёнка_с_маком',
                         'Плюшка',
                         'Растегай',
                         'Рогалик',
                         'Рулет_с_маком',
                         'Тесто_Пирожковое_охлажденное',
                         'Пряники']
list_name_brod2_dop = [
    'Ватрушка_с_творогом',
    'Ватрушка_с_сыром',
    'Ватрушка_с_конфитюром',
    'Беляш_печеный',
    'Кекс_классический',
    'Кекс_шоколадный',
    'Кулебяка',
    'Пирог_с_капустой',
    'Пирог_с_яблоками',
    'Пицца_мини',
    'Ромовая_баба',
    'Сосиска_в_тесте']
list_name_brod2_osnov_print = ['Клиент',
                               'Сдоб',
                               'Фран',
                               'Бога',
                               'Богк',
                               'Дарк',
                               'Кл75',
                               'Кл50',
                               'Кл35',
                               'Куиз',
                               'Кутм',
                               'Овся',
                               'Степ',
                               'Тост',
                               'Чиаб',
                               'Яров',
                               'Кчаю',
                               'Кори',
                               'Коркр',
                               'Счес',
                               'гамб',
                               'хотд',
                               'Плет',
                               'Плюш',
                               'Раст',
                               'Рога',
                               'Руле',
                               'Тест',
                               'Прян']
list_name_brod2_dop_print = ['Клиент',
                             'Ватв',
                             'Васы',
                             'Вако',
                             'Беля',
                             'КеКл',
                             'КеШо',
                             'Куле',
                             'ПиКа',
                             'ПиЯб',
                             'Пицц',
                             'Ромо',
                             'Соси']

ADMIN = 1914231330

# Приветсивенный текст
hi_text = 'Привет наш бот может принять заявку на хлеб и поделиться информацией!'


# функция информирующая о запуске бота
async def on_startup(_):
    print('Погнали!')


# функция очистки переменных списков
def clear_list_app():
    # восстанавливаем значение списка заявок в первоначальное состояние
    if len(list_application1) > 0:
        for ind in range(0, len(list_application1)):
            list_application1[ind] = 0

    # и очистим за собой это список чтобы можно было еще делать заявку
    if len(id_and_name_clients) > 0:
        for i in range(len(id_and_name_clients)):
            del id_and_name_clients[0]

    # востонавливаем значение списка id_and_name_clients2
    if len(id_and_name_clients2) > 1:
        for ind in range(len(id_and_name_clients2)):
            del id_and_name_clients[0]

    # восстанавливаем пустой список
    if len(id_clients_end_day_of_weec_permanent_applications) > 0:
        for i in range(len(id_clients_end_day_of_weec_permanent_applications)):
            del id_clients_end_day_of_weec_permanent_applications[0]


########################################################################################################################


# ЗАЯВКА
########################################################################################################################
# этот хендлер обрабатывает только фразу 'Сделать_заявку' и выдаёт первый список хлеба
@dp.message_handler(Text(equals='Сделать  🍞/ изменить заявку'))
async def cdm_make_application(message: types.Message):
    await message.delete()
    ind_list1 = 0
    ind_list2 = 0
    await message.answer(
        text='Начало списка____________________',
        reply_markup=keyboard.back_cart_confirm(),  # клавиатура закрывается после наж.
    )
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

    for brod in list_name_brod_osnov:
        await message.answer(text=f'<b>{brod}</b>',  # пишем текст
                             reply_markup=keyboard.get_iline_keyboard(ind_list2, ind_list1),
                             parse_mode="HTML")  # запускаем ин лайн клавиатуру
        ind_list2 += 1
    await message.answer(text='Конец списка_____________________')


# Удалить заявку
@dp.message_handler(Text(equals='Удалить заявку'))
async def del_application(message: types.Message):
    await message.delete()
    ind_list1 = 0
    ind_list2 = 0

    # получим имя клиента
    name_and_id_clients = bd.name_and_id_clients(message.from_user.id)

    # зайдем в bd и узнаем, существует ли заявка для этого клиента
    applications = bd.applications_true_falshe(name_and_id_clients[1])

    # если была заявка:
    if applications == True:
        # зайдем в bd и удалим заявку
        result = bd.del_applications(name_and_id_clients[0])
        if result == True:
            await message.answer(text=f'Вы успешно удалили заявку для: {name_and_id_clients[1]}!')

    else:
        await message.answer(text=f'Заявки для клиента: {name_and_id_clients} не существует!',
                             reply_markup=keyboard.kb_menu())


# '+' к заявке
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('+'))
async def ikb_cd_handler(callback: types.CallbackQuery):
    # проверим под каким индексом находится хлеб в списке
    # если длина данных с кнопки не больше двух символов(первый '+')
    if len(callback.data) == 2:
        # тогда прибавляем к заказу по индексу int(callbeck.data[1]),+1 в списке заказов
        list_application1[int(callback.data[1])] += 1
        # затем меняем текст шапки(незнаю можно ли обойтись без этого) и перезаписываем клавиатуру
        await callback.message.edit_text(text=f'<b>{list_name_brod_osnov[int(callback.data[1])]}</b>',
                                         reply_markup=keyboard.get_iline_keyboard(callback.data[1],
                                                                                  list_application1[
                                                                                      int(callback.data[1])]),
                                         parse_mode="HTML")

    # если длина данных с кнопки ровна 3 символам(первый '+', второй '1')
    elif len(callback.data) == 3 and int(callback.data[1]) == 1:
        list_application1[10 + int(callback.data[2])] += 1
        await callback.message.edit_text(
            text=f'<b>{list_name_brod_osnov[10 + int(callback.data[2])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(10 + int(callback.data[2]),
                                                     list_application1[10 + int(callback.data[2])]),
            parse_mode="HTML")
    # если длина данных с кнопки ровна 3 символам(первый '+', второй '2')
    elif len(callback.data) == 3 and int(callback.data[1]) == 2:
        list_application1[20 + int(callback.data[2])] += 1
        await callback.message.edit_text(
            text=f'<b>{list_name_brod_osnov[20 + int(callback.data[2])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(20 + int(callback.data[2]),
                                                     list_application1[20 + int(callback.data[2])]),
            parse_mode="HTML")  # пишем текст
    # если длина данных с кнопки ровна 3 символам(первый '+', второй '3')
    elif len(callback.data) == 3 and int(callback.data[1]) == 3:
        list_application1[30 + int(callback.data[2])] += 1
        await callback.message.edit_text(
            text=f'<b>{list_name_brod_osnov[30 + int(callback.data[2])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(30 + int(callback.data[2]),
                                                     list_application1[30 + int(callback.data[2])]),
            parse_mode="HTML")  # пишем текст


# '-' к заявке
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('-'))
async def ikb_cd_handler(callbeck: types.CallbackQuery):
    # если длина данных с кнопки не больше двух символов(первый '-')
    if len(callbeck.data) == 2:
        if list_application1[int(callbeck.data[1])] != 0:
            list_application1[int(callbeck.data[1])] -= 1
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[int(callbeck.data[1])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(callbeck.data[1],
                                                     list_application1[int(callbeck.data[1])]),
            parse_mode="HTML")
    # если длина данных с кнопки ровна 3 символам(первый '-', второй '1')
    elif len(callbeck.data) == 3 and int(callbeck.data[1]) == 1:
        # если значение в списке заявок не ровно нулю тогда можно отнять 1 от заявки
        if list_application1[10 + int(callbeck.data[2])] != 0:
            list_application1[10 + int(callbeck.data[2])] -= 1
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[10 + int(callbeck.data[2])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(10 + int(callbeck.data[2]),
                                                     list_application1[10 + int(callbeck.data[2])]),
            parse_mode="HTML")
    # если длина данных с кнопки ровна 3 символам(первый '-', второй '2')
    elif len(callbeck.data) == 3 and int(callbeck.data[1]) == 2:
        if list_application1[20 + int(callbeck.data[2])] != 0:
            list_application1[20 + int(callbeck.data[2])] -= 1
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[20 + int(callbeck.data[2])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(20 + int(callbeck.data[2]),
                                                     list_application1[20 + int(callbeck.data[2])]),
            parse_mode="HTML")

    # если длина данных с кнопки ровна 3 символам(первый '-', второй '3')
    elif len(callbeck.data) == 3 and int(callbeck.data[1]) == 3:
        if list_application1[30 + int(callbeck.data[2])] != 0:
            list_application1[30 + int(callbeck.data[2])] -= 1
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[30 + int(callbeck.data[2])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(30 + int(callbeck.data[2]),
                                                     list_application1[30 + int(callbeck.data[2])]),
            parse_mode="HTML")


# '+10' к заявке
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('10+'))
async def ikb_cd_handler(callback: types.CallbackQuery):
    id = callback.from_user.id
    # проверим под каким индексом находится хлеб в списке
    # если длина данных с кнопки не больше двух символов(первый '+')
    if len(callback.data) == 4:
        # тогда прибавляем к заказу по индексу int(callbeck.data[1]),+1 в списке заказов
        list_application1[int(callback.data[3])] += 10
        # затем меняем текст шапки(незнаю можно ли обойтись без этого) и перезаписываем клавиатуру
        await callback.message.edit_text(text=f'<b>{list_name_brod_osnov[int(callback.data[3])]}</b>',
                                         reply_markup=keyboard.get_iline_keyboard(callback.data[3],
                                                                                  list_application1[
                                                                                      int(callback.data[3])]),
                                         parse_mode="HTML")

    # если длина данных с кнопки ровна 3 символам(первый '+', второй '1')
    elif len(callback.data) == 5 and int(callback.data[3]) == 1:
        list_application1[10 + int(callback.data[4])] += 10
        await callback.message.edit_text(
            text=f'<b>{list_name_brod_osnov[10 + int(callback.data[4])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(10 + int(callback.data[4]),
                                                     list_application1[10 + int(callback.data[4])]),
            parse_mode="HTML")
    # если длина данных с кнопки ровна 3 символам(первый '+', второй '2')
    elif len(callback.data) == 5 and int(callback.data[3]) == 2:
        list_application1[20 + int(callback.data[4])] += 10
        await callback.message.edit_text(
            text=f'<b>{list_name_brod_osnov[20 + int(callback.data[4])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(20 + int(callback.data[2]),
                                                     list_application1[20 + int(callback.data[4])]),
            parse_mode="HTML")  # пишем текст
    # если длина данных с кнопки ровна 3 символам(первый '+', второй '3')
    elif len(callback.data) == 5 and int(callback.data[3]) == 3:
        list_application1[30 + int(callback.data[4])] += 10
        await callback.message.edit_text(
            text=f'<b>{list_name_brod_osnov[30 + int(callback.data[4])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(30 + int(callback.data[4]),
                                                     list_application1[30 + int(callback.data[4])]),
            parse_mode="HTML")  # пишем текст


# '-10' к заявке
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('10-'))
async def ikb_cd_handler(callbeck: types.CallbackQuery):
    # если длина данных с кнопки не больше двух символов(первый '-')
    if len(callbeck.data) == 4:
        if list_application1[int(callbeck.data[3])] != 0 or list_application1[int(callbeck.data[3])] >= 10:
            list_application1[int(callbeck.data[3])] -= 10
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[int(callbeck.data[3])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(callbeck.data[3],
                                                     list_application1[int(callbeck.data[3])]),
            parse_mode="HTML")
    # если длина данных с кнопки ровна 3 символам(первый '-', второй '1')
    elif len(callbeck.data) == 5 and int(callbeck.data[3]) == 1:
        # если значение в списке заявок не ровно нулю тогда можно отнять 1 от заявки
        if list_application1[10 + int(callbeck.data[4])] != 0 or list_application1[10 + int(callbeck.data[4])] >= 10:
            list_application1[10 + int(callbeck.data[4])] -= 10
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[10 + int(callbeck.data[4])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(10 + int(callbeck.data[4]),
                                                     list_application1[10 + int(callbeck.data[4])]),
            parse_mode="HTML")
    # если длина данных с кнопки ровна 3 символам(первый '-', второй '2')
    elif len(callbeck.data) == 5 and int(callbeck.data[3]) == 2:
        if list_application1[20 + int(callbeck.data[4])] != 0 or list_application1[20 + int(callbeck.data[4])] >= 10:
            list_application1[20 + int(callbeck.data[4])] -= 10
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[20 + int(callbeck.data[4])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(20 + int(callbeck.data[4]),
                                                     list_application1[20 + int(callbeck.data[4])]),
            parse_mode="HTML")

    # если длина данных с кнопки ровна 3 символам(первый '-', второй '3')
    elif len(callbeck.data) == 5 and int(callbeck.data[3]) == 3:
        if list_application1[30 + int(callbeck.data[4])] != 0 or list_application1[30 + int(callbeck.data[4])] >= 10:
            list_application1[30 + int(callbeck.data[4])] -= 10
        await callbeck.message.edit_text(
            text=f'<b>{list_name_brod_osnov[30 + int(callbeck.data[4])]}</b>',
            reply_markup=keyboard.get_iline_keyboard(30 + int(callbeck.data[4]),
                                                     list_application1[30 + int(callbeck.data[4])]),
            parse_mode="HTML")


# 'Подтверждение заявки'
@dp.message_handler(Text(equals='Подтвердить 💰'))
async def reg_aplikations(message: types.Message):
    await message.delete()
    # получим имя клиента и его индекс из bd
    id_clients = bd.name_and_id_clients(message.from_user.id)[0]
    name_clients = bd.name_and_id_clients(message.from_user.id)[1]

    # создадим таблицу для основной заявки если её ещё нет в bd
    result_create_aplication = bd.create_request_table(id_clients, name_clients, list_application1)
    if result_create_aplication == True:
        await message.answer(text=f'Вы успешно зарегистрировали заявку для:\n{name_clients}',
                             reply_markup=keyboard.kb_menu())
        # восстанавливаем значение списка заявок в первоначальное состояние
        for ind in range(0, len(list_application1)):
            list_application1[ind] = 0
    else:
        await message.answer(text=f'Для "{name_clients}" уже создана заявка')
        await message.answer(text='Перезаписать?',
                             reply_markup=keyboard.get_iline_keyboard_yes_no_look())


# Корзина
@dp.message_handler(Text(equals='Корзина 🛒'))
async def basket(message: types.Message):
    await message.delete()

    # узнаем id клиента(славгород или яровое) из bd
    id_klients = bd.name_and_id_clients(message.from_user.id)
    # если id клиента относится к яровому тогда возьмем Яровские цены хлеба из таблицы Хлеб и поместим их в список
    if id_klients[0] < 22:
        list_prise = bd.price_jrovoe_list()

    # если id клиента относится к Славгороду тогда возьмем Славгородские цены хлеба из таблицы Хлеб и поместим их в список
    else:
        list_prise = bd.price_slavgorod_list()

    # создадим список для подсчета суммы заявки
    ind = 0
    list_summ_aplication = []
    # пройдемся по списку заявки и где она есть перемножим с ценой и поместим это значение в список для подсчета
    for i in list_application1:
        if i > 0:
            await message.answer(
                text=f'{list_name_brod_osnov[ind]} - {i}шт * {list_prise[ind]} = {i * list_prise[ind]} рублей')
            list_summ_aplication.append(i * list_prise[ind])
        ind += 1
    summ = 0
    for i in list_summ_aplication:
        summ += i
    await message.answer(text=f'Итого {summ}')
    await message.answer(text=f'Если всё верно нажмите "Подтвердить"')


#  Да, Нет, посмотреть старую заявку - на вопрос'перезаписать заявку'
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('!'))
async def ikb_cd_handler(callback: types.CallbackQuery):
    # получим имя клиента и его индекс
    id_clients = bd.name_and_id_clients(callback.from_user.id)[0]
    name_clients = bd.name_and_id_clients(callback.from_user.id)[1]
    # если ответили 'Да'
    if callback.data[1] == 'Д':
        # зайдем в bd и исправим заявку
        bd.change_old_aplikation(id_clients, list_application1)
        await callback.message.answer(text='Вы успешно перезаписали заявку!',
                                      reply_markup=keyboard.kb_menu())
        # востонавливаем значение списка заявок в первоначальное состаяние
        for ind in range(0, len(list_application1)):
            list_application1[ind] = 0

    # если ответили нет
    elif callback.data[1] == 'Н':
        await callback.message.answer(text='Хорошо мы оставим предыдущую запись!',
                                      reply_markup=keyboard.kb_menu())

        # востонавливаем значение списка заявок в первоначальное состаяние
        for ind in range(0, len(list_application1)):
            list_application1[ind] = 0

    # если ответили - посмотреть старую заявку
    elif callback.data[1] == 'С':

        # если id клиента относится к яровому тогда возьмем из bd Яровские цены хлеба и поместим их в список
        if id_clients < 22:
            list_prise = bd.price_jrovoe_list()

        # если id клиента относится к Славгороду тогда возьмем из bd Славгородские цены хлеба и поместим их в список
        else:
            list_prise = bd.price_slavgorod_list()

        # создадим список и поместим в него старую заявку из bd
        list_old_aplication = bd.old_aplication(name_clients)

        # создадим список для подсчета суммы заявки
        ind = 0
        list_summ_aplication = []

        # пройдемся по списку заявки и где она есть перемножим с ценой и поместим это значение в список для подсчета
        for i in list_old_aplication:

            if i > 0 and i:
                await callback.message.answer(
                    text=f'{list_name_brod_osnov[ind]} - {i}шт * {list_prise[ind]} = {i * list_prise[ind]} рублей')
                list_summ_aplication.append(i * list_prise[ind])
            ind += 1
        summ = 0
        for i in list_summ_aplication:
            summ += i
        await callback.message.answer(text=f'Итого {summ}')
        await callback.message.answer(text='Перезаписать заявку?',
                                      reply_markup=keyboard.get_iline_keyboard_yes_no())


########################################################################################################################


# КЛИЕНТ МЕНЮ
########################################################################################################################

# этот хендлер обрабатывает только фразу 'назад'
@dp.message_handler(Text(equals='⬅️назад '))
async def reg(message: types.Message):
    await message.delete()
    await message.answer(text='_________________________________',
                         reply_markup=keyboard.kb_menu())
    await message.delete()


# этот хендлер обрабатывает только фразу 'Контакты ☎️'
@dp.message_handler(Text(equals='Контакты ☎️'))
async def reg(message: types.Message):
    await message.delete()
    await message.answer(text=kontakts,
                         parse_mode="HTML")


# этот хендлер обрабатывает только фразу 'Вакансии 👤'
@dp.message_handler(Text(equals='Вакансии 👤'))
async def reg(message: types.Message):
    await message.delete()
    await message.answer(text=vacancies,
                         parse_mode="HTML")


# этот хендлер обрабатывает только фразу 'Прайс-Яровое 🥨'
@dp.message_handler(Text(equals='Прайс-Яровое 🥨'))
async def reg(message: types.Message):
    await message.delete()

    # зайдем в bd, скачаем Яровские цены и поместим их в список
    price_jrovoe = bd.price_jrovoe()

    # создадим два списка и поместим в них информацию из прайса
    price_brod_1 = ''
    price_brod_2 = ''
    # создадим переменную для сохранения индекса из списка 'x', из-за невозможности обработать больше 20 строк (HTML)
    index_x = 0
    for i in price_jrovoe:
        if index_x < 20:
            index_x += 1
            price_brod_1 = f'{price_brod_1}<b>{i[1]}:\n</b>' \
                           f'<em>вес</em> - {i[2]}г, ' \
                           f'<em>цена</em> - {i[3]}р;\n'
        elif index_x > 19 or index_x < 42:
            price_brod_2 = f'{price_brod_2}<b>{i[1]}:\n</b>' \
                           f'<em>вес</em> - {i[2]}г, ' \
                           f'<em>цена</em> - {i[3]}р;\n'
    await message.answer(text=price_brod_1,
                         parse_mode="HTML")
    await message.answer(text=price_brod_2,
                         parse_mode="HTML")


# этот хендлер обрабатывает только фразу 'Прайс-Славгород 🥐'
@dp.message_handler(Text(equals='Прайс-Славгород 🍪'))
async def reg(message: types.Message):
    await message.delete()
    price_slavgorod = bd.price_slavgorod()
    # создадим переменную для сохранения индекса из списка 'x', из-за невозможности обработать больше 20 строк (HTML)
    index_x = 0
    # создадим переменные для сохранения информации из bd(наименование, вес, цена)
    price_brod_1 = ''
    price_brod_2 = ''
    # помещаем информацию и списка
    for i in price_slavgorod:
        if index_x < 20:
            index_x += 1
            price_brod_1 = f'{price_brod_1}<b>{i[1]}:\n</b>' \
                           f'<em>вес</em> - {i[2]}г, ' \
                           f'<em>цена</em> - {i[3]}р;\n'
        elif index_x > 19 or index_x < 42:
            price_brod_2 = f'{price_brod_2}<b>{i[1]}:\n</b>' \
                           f'<em>вес</em> - {i[2]}г, ' \
                           f'<em>цена</em> - {i[3]}р;\n'
    await message.answer(text=price_brod_1,
                         parse_mode="HTML")
    await message.answer(text=price_brod_2,
                         parse_mode="HTML")


# # этот хендлер обрабатывает только фразу 'Прайс с Фото 📷 (Яровое, Славгород)'
@dp.message_handler(Text(equals='Прайс с Фото 📷 (Яровое, Славгород)'))
async def reg(message: types.Message):
    await message.delete()
    # из bd возьмем прайс
    price = bd.price()

    # пройдемся по списку и через цикл выдадим сформированное сообщение(прайс) с фото или нет
    for brod in price:
        if brod[5] != '':
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=brod[5],
                                 caption=f'<em>Название:</em> <b>{brod[1]}</b>\n'
                                         f'<em>Вес:</em> {brod[2]} гр.\n'
                                         f'<em>Цена для Ярового:</em> {brod[3]} руб.\n'
                                         f'<em>Цена для Славгорода:</em> {brod[4]} руб.\n',
                                 parse_mode="HTML",
                                 )
        else:
            await message.answer(text=f'<em>Название:</em> <b>{brod[1]}</b>\n'
                                      f'<em>Вес:</em> {brod[2]} гр.\n'
                                      f'<em>Цена для Ярового:</em> {brod[3]} руб.\n'
                                      f'<em>Цена для Славгорода:</em> {brod[4]} руб.\n',
                                 parse_mode="HTML")
    await message.answer(text='Ждем ваших заявок!☎️🍪😁')


# этот хендлер обрабатывает только фразу 'Оставить отзыв и предложения 💌''
@dp.message_handler(Text(equals='Оставить отзыв и предложения 💌'))
async def reg(message: types.Message):
    await message.delete()
    await message.answer(text='Напишите ваш отзыв или предложение в поле ввода текста и отправьте его.'
                              'Наш менеджер 👤 обязательно обработает ваше сообщение!'
                              'Всего доброго!')


# этот хендлер обрабатывает отзыв клиента
@dp.message_handler(Text(contains='#'))
async def reg(message: types.Message):
    await message.answer(text='Спасибо за отзыв!')

    # получим имя клиента и его индекс
    id_clients = bd.name_and_id_clients(message.from_user.id)[0]
    name_clients = bd.name_and_id_clients(message.from_user.id)[1]
    # заполняем таблицу с отзывами в бд
    bd.registration_review(id_clients, name_clients, message.text)
    # бот отправляет сообщение с отзывом мне
    await bot.send_message(ADMIN, f'Отправитель: {name_clients}\nСообщение:{message.text}')


########################################################################################################################


# АДМИН МЕНЮ
########################################################################################################################

# menu 'ЗАЯВКИ'
@dp.message_handler(Text(contains='Заявки'))
async def admin_application(message: types.Message):
    await message.delete()
    await message.answer(text='Вы зашли в меню "Заявки"',
                         reply_markup=keyboard.kb_menu_application_admin())


# создадим словарь куда, будем помещать изменения по клиенту
CLIENTS = {}


# menu 'Заявки' - добавить
@dp.message_handler(Text(contains='Добавить + 📝, Изменить 🔄'))
async def add_application(message: types.Message):
    await message.delete()

    # возьмём из bd список клиентов и выдадим для выбора по id (нужно напечатать)
    list_clients = bd.id_and_name_all_clients()
    list_str_clients = ''
    for id_and_name in list_clients:
        list_str_clients = f'{list_str_clients}\n' \
                           f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Клиенты:</b>\n'
                              f'{list_str_clients}',
                         parse_mode="HTML")
    await message.answer(text='Введите id клиента:')
    await FSMAdmin_applications_add.Id.set()


# 'Заявки' - добавить - ловим id клиента
@dp.message_handler(state=FSMAdmin_applications_add.Id)
async def catch_id_clients(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['id'] = int(message.text)

    # возьмем id и найдем по нему имя из bd
    CLIENTS['name_clients'] = bd.name_clients(CLIENTS['id'])

    # зпустим инлайн заявку
    ind_list1 = 0
    ind_list2 = 0
    await message.answer(
        text='Начало списка____________________',
        reply_markup=keyboard.back_cart_confirm_admin(),  # клавиатура закрывается после наж.
    )
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

    for brod in list_name_brod_osnov:
        await message.answer(text=f'<b>{brod}</b>',  # пишем текст
                             reply_markup=keyboard.get_iline_keyboard(ind_list2, ind_list1),
                             parse_mode="HTML")  # запускаем инлайн клавиатуру
        ind_list2 += 1

    await message.answer(text='Конец списка_____________________')
    await state.finish()


@dp.message_handler(Text(equals='Подтвердить ✍️'))
async def reg_applikations(message: types.Message):
    await message.delete()
    # получим имя клиента и его индекс из bd
    id_clients = CLIENTS['id']
    name_clients = CLIENTS["name_clients"]

    # запишем только что полученные id и name в список для внесения мзменений в щаявку через бд
    for i in (id_clients, name_clients):
        id_and_name_clients2.append(i)

    # создадим таблицу для основной заявки если её ещё нет в bd
    result_create_aplication = bd.create_request_table(id_clients, name_clients, list_application1)
    if result_create_aplication == True:
        await message.answer(text=f'Вы успешно зарегистрировали заявку для:\n{name_clients}',
                             reply_markup=keyboard.kb_menu_admin())

        # восстанавливаем значение списка заявок в первоначальное состояние
        clear_list_app()

    else:
        await message.answer(text=f'Для "{name_clients}" уже создана заявка')
        await message.answer(text='Перезаписать ⁉',
                             reply_markup=keyboard.get_inline_keyboard_yes_no_look_admin())
    CLIENTS.clear()


# Да, Нет, посмотреть старую заявку - на вопрос 'перезаписать заявку'
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('?'))
async def yes_no_look(callback: types.CallbackQuery):
    # получим имя клиента и его индекс
    id_clients = id_and_name_clients2[0]
    name_clients = id_and_name_clients2[1]
    # если ответили 'Да'
    if callback.data[1] == 'Д':
        # зайдем в bd и исправим заявку
        bd.change_old_aplikation(id_clients, list_application1)
        await callback.message.answer(text='Вы успешно перезаписали заявку!',
                                      reply_markup=keyboard.kb_menu_admin())

        # востонавливаем значение списка заявок в первоначальное состаяние
        clear_list_app()

    # если ответили нет
    elif callback.data[1] == 'Н':
        await callback.message.answer(text='Хорошо мы оставим предыдущую запись!',
                                      reply_markup=keyboard.kb_menu_admin())

        # востонавливаем значение списка заявок в первоначальное состаяние
        clear_list_app()

    # если ответили - посмотреть старую заявку
    elif callback.data[1] == 'С':

        # если id клиента относится к яровому тогда возьмем из bd Яровские цены хлеба и поместим их в список
        if int(id_clients) < 22:
            list_prise = bd.price_jrovoe_list()

        # если id клиента относится к Славгороду тогда возьмем из bd Славгородские цены хлеба и поместим их в список
        else:
            list_prise = bd.price_slavgorod_list()

        # создадим список и поместим в него старую заявку из bd
        list_old_aplication = bd.old_aplication(name_clients)

        # создадим список для подсчета суммы заявки
        ind = 0
        list_summ_aplication = []

        # пройдемся по списку заявки и где она есть перемножим с ценой и поместим это значение в список для подсчета
        for i in list_old_aplication:

            if i > 0 and i:
                await callback.message.answer(
                    text=f'{list_name_brod_osnov[ind]} - {i}шт * {list_prise[ind]} = {i * list_prise[ind]} рублей')
                list_summ_aplication.append(i * list_prise[ind])
            ind += 1
        summ = 0
        for i in list_summ_aplication:
            summ += i
        await callback.message.answer(text=f'Итого {summ}')
        await callback.message.answer(text='Перезаписать заявку?',
                                      reply_markup=keyboard.get_iline_keyboard_yes_no_admin())


# Корзина
@dp.message_handler(Text(equals='Корзина 🗑'))
async def basket(message: types.Message):
    await message.delete()

    # узнаем id клиента(славгород или яровое) из bd
    id_klients = CLIENTS['id']

    # если id клиента относится к яровому тогда возьмем Яровские цены хлеба из таблицы Хлеб и поместим их в список
    if int(id_klients) < 22:
        list_prise = bd.price_jrovoe_list()

    # если id клиента относится к Славгороду тогда возьмем Славгородские цены хлеба из таблицы Хлеб и поместим их в список
    else:
        list_prise = bd.price_slavgorod_list()

    # создадим список для подсчета суммы заявки
    ind = 0
    list_summ_aplication = []
    # пройдемся по списку заявки и где она есть перемножим с ценой и поместим это значение в список для подсчета
    for i in list_application1:
        if i > 0:
            await message.answer(
                text=f'{list_name_brod_osnov[ind]} - {i}шт * {list_prise[ind]} = {i * list_prise[ind]} рублей')
            list_summ_aplication.append(i * list_prise[ind])
        ind += 1
    summ = 0
    for i in list_summ_aplication:
        summ += i
    await message.answer(text=f'Итого {summ}')


# 'Заявки' - удалить
@dp.message_handler(Text(equals='Удалить 🗑'))
async def clear_app(message: types.Message):
    await message.delete()

    # возьмём из bd список клиентов и выдадим для выбора по id (нужно напечатать)
    list_clients = bd.id_and_name_all_clients()
    list_str_clients = ''
    for id_and_name in list_clients:
        list_str_clients = f'{list_str_clients}\n' \
                           f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Клиенты:</b>\n'
                              f'{list_str_clients}',
                         parse_mode="HTML")
    await message.answer(text='Введите id клиента')
    await FSMAdmin_applications_del.Id.set()


# 'Заявки' - удалить - ловим id клиента
@dp.message_handler(state=FSMAdmin_applications_del.Id)
async def catch_id_clients(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['id'] = int(message.text)

    # возьмем id и найдем по нему имя из bd
    CLIENTS['name_clients'] = bd.name_clients(CLIENTS['id'])

    # зайдем в bd и удалим запись по id

    bd.del_applications(CLIENTS['id'])

    # выводим инлайн клавиатуру с днями недели
    await message.answer(text=f'Заявка для {CLIENTS["name_clients"]} на завтра, успешно УДАЛЕНА!!!',
                         reply_markup=keyboard.kb_menu_admin())
    await state.finish()


#
# # 'Заявки'- Удалить - ловим ID клиента, чтобы удалить его
# @dp.message_handler(Text(contains='ud'))
# async def get_days_of_week(message: types.Message):
#     # возьмем id из нашего сообщения и найдем по нему имя из bd
#     id_clients = message.text[2:len(message.text)]
#     name_clients = bd.name_clients(id_clients)
#
#     # зайдем в bd и удалим запись по id
#
#     bd.del_applications(id_clients)
#
#     # выводим инлайн клавиатуру с днями недели
#     await message.answer(text=f'Заявка для {name_clients} на завтра, успешно УДАЛЕНА!!!',
#                          reply_markup=keyboard.kb_menu_admin())


# menu 'ПОСТОЯННЫЕ ЗАЯВКИ'
@dp.message_handler(Text(contains='Постоянные заявки'))
async def admin_application(message: types.Message):
    await message.delete()
    await message.answer(text='Вы зашли в меню "Постоянные заявки"',
                         reply_markup=keyboard.kb_menu_constant_application_admin())


# 'Постоянные заявки' - добавить
@dp.message_handler(Text(contains='Добавить 🖌, Изменить 🔄'))
async def add_application(message: types.Message):
    await message.delete()

    # возьмём из bd список клиентов и выдадим для выбора по id (нужно напечатать)
    list_clients = bd.id_and_name_all_clients()
    list_str_clients = ''
    for id_and_name in list_clients:
        list_str_clients = f'{list_str_clients}\n' \
                           f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Клиенты:</b>\n'
                              f'{list_str_clients}',
                         parse_mode="HTML")
    await message.answer(text='Введите id клиента:')

    await FSMAdmin_constant_applications_add.Id.set()


# 'Постоянные заявки'- добавить - ловим ID клиента и выдаем клавиатуру с днями недели для выбора
@dp.message_handler(state=FSMAdmin_constant_applications_add.Id)
async def get_days_of_week(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['id'] = int(message.text)
    # возьмем id из нашего сообщения и найдем по нему имя
    CLIENTS['name_clients'] = bd.name_clients(CLIENTS['id'])

    # выводим инлайн клавиатуру с днями недели
    await message.answer(text='Выберете день недели 🗓',
                         reply_markup=keyboard.get_inline_keyboard_deys_of_week('add'))
    await state.finish()


# 'Постоянные заявки'- добавить - ловим день недели и выдаем инлайн кл для заявки с данными(старой заявкой)
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('add'))
async def get_application(callback: types.CallbackQuery):
    # присваиваем переменным название дня недели
    CLIENTS['name_table'] = callback.data[3:len(callback.data)]
    id_clients = CLIENTS['id']

    # подгрузим старую заявку в виде списка в переменную
    list_permanent_applications = bd.permanent_applications(id_clients, CLIENTS['name_table'])

    # если не оказалась старой заявки, то загрузим пустые значения
    if len(list_permanent_applications) < 2:
        ind_list1 = 0
        ind_list2 = 0
        for brod in list_name_brod_osnov:
            await callback.message.answer(text=f'<b>{brod}</b>',  # пишем текст
                                          reply_markup=keyboard.get_iline_keyboard(ind_list2, ind_list1),
                                          parse_mode="HTML")  # запускаем инлайн клавиатуру
            ind_list2 += 1
        await callback.message.answer(text='Конец списка_____________________',
                                      reply_markup=keyboard.confirm_applications())

    # если уже есть заявка на это день, то подставим эти значения
    else:
        # удалим из старого списка ID и NAME
        del list_permanent_applications[0]
        del list_permanent_applications[0]
        # запишим значения старой заявки в list_applications1
        ind = 0
        for x in list_permanent_applications:
            list_application1.insert(ind, x)
            ind += 1

        ind_list1 = 0
        ind_list2 = 0
        for brod in list_name_brod_osnov:
            await callback.message.answer(text=f'<b>{brod}</b>',  # пишем текст
                                          reply_markup=keyboard.get_iline_keyboard(ind_list2,
                                                                                   list_application1[ind_list1]),
                                          parse_mode="HTML")  # запускаем инлайн клавиатуру
            ind_list2 += 1
            ind_list1 += 1
        await callback.message.answer(text='Конец списка_____________________',
                                      reply_markup=keyboard.confirm_applications())


# 'Постоянные заявки'- добавить- Подтверждение постоянной заявки
@dp.message_handler(Text(equals='Подтвердить!'))
async def admin_application(message: types.Message):
    await message.delete()
    # получим имя клиента и его индекс из переменной id_clients_end_day_of_weec_permanent_applications
    id_clients = CLIENTS['id']
    name_clients = CLIENTS['name_clients']
    name_table = CLIENTS['name_table']

    # запишем нашу постоянную заявку в bd
    result_create_application = bd.save_permanent_applications(id_clients, name_clients, list_application1, name_table)
    if result_create_application == True:
        await message.answer(text=f'Вы успешно зарегистрировали постоянную заявку для:\n{name_clients}\n'
                                  f'в(во): {name_table}',
                             reply_markup=keyboard.kb_menu_admin())
        # восстанавливаем значение списка заявок в первоначальное состояние
        clear_list_app()
    # очистим словарь
    CLIENTS.clear()


# 'Постоянные заявки' - Удалить
@dp.message_handler(Text(equals='Удалить 🚮'))
async def add_application(message: types.Message):
    await message.delete()

    # возьмём из bd список клиентов и выдадим для выбора по id (нужно напечатать)
    list_clients = bd.id_and_name_all_clients()
    list_str_clients = ''
    for id_and_name in list_clients:
        list_str_clients = f'{list_str_clients}\n' \
                           f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Клиенты:</b>\n'
                              f'{list_str_clients}',
                         parse_mode="HTML")
    await message.answer(text='Введите id клиента')

    await FSMAdmin_constant_applications_del.Id.set()


# 'Постоянные заявки'- Удалить - ловим ID клиента, чтобы удалить его
@dp.message_handler(state=FSMAdmin_constant_applications_del.Id)
async def get_days_of_week(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['id'] = int(message.text)
    # возьмем id из нашего сообщения и найдем по нему имя из bd
    CLIENTS['name_clients'] = bd.name_clients(CLIENTS['id'])

    # выводим инлайн клавиатуру с днями недели
    await message.answer(text='Выберете день недели 🗓',
                         reply_markup=keyboard.get_inline_keyboard_deys_of_week('del'))
    await state.finish()


# 'Постоянные заявки'- Удалить - ловим день недели и удаляем постоянную заявку
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('del'))
async def get_aplication(callback: types.CallbackQuery):
    # присваиваем переменным id и название дня недели
    id_clients = CLIENTS['id']
    name_table = callback.data[3:len(callback.data)]
    name_clients = CLIENTS['name_clients']

    # заходим в bd и удаляем постоянную заявку по id
    result = bd.del_permanent_applications(id_clients, name_table)

    if result == True:
        await callback.message.answer(text=f'Вы успешно удалили постоянную заявку для {name_clients}\n'
                                           f'в(во) - {name_table}')
    else:
        await callback.message.answer(text=f'Что-то пошло не так!')

    # очистим наши вспомогательные списки
    clear_list_app()
    CLIENTS.clear()


# menu 'КЛИЕНТЫ'
@dp.message_handler(Text(equals='Клиенты 👤'))
async def admin_application(message: types.Message):
    await message.delete()
    await message.answer(text='Вы зашли в меню "Клиенты"',
                         reply_markup=keyboard.kb_menu_clients_admin())


# Клиенты - добавить
@dp.message_handler(Text(equals='Добавить + 👤', ignore_case=True), state=None)
async def start_work(message: types.Message):
    await FSMAdmin_Clients.Name.set()
    await message.answer('Напишите имя клиента например - ООО Колос',
                         reply_markup=keyboard.get_cancel())


# Выход из машины состояний
@dp.message_handler(commands=['cancel'], state='*')  # если нажали cancel в любом из состаяний
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state == None:
        return

    await state.finish()
    await message.reply('Вы прервали ввод данных!',
                        reply_markup=keyboard.kb_menu_admin())


# МАШИНА СОСТОЯНИЙ - добавление клиента ############
@dp.message_handler(state=FSMAdmin_Clients.Name)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await FSMAdmin_Clients.next()
    await message.reply('Запишите номер телефона')


@dp.message_handler(state=FSMAdmin_Clients.Phone_number)
async def add_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Phone_number'] = message.text
    await FSMAdmin_Clients.next()
    await message.reply('А теперь добавьте адрес клиента')


@dp.message_handler(state=FSMAdmin_Clients.Address)
async def add_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Address'] = message.text
    await FSMAdmin_Clients.next()
    await message.reply('И название магазина')


@dp.message_handler(state=FSMAdmin_Clients.Name_shop)
async def add_name_shop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name_shop'] = message.text

    await FSMAdmin_Clients.next()
    await message.answer('Введите город:(Яровое, Славгород)')


x = ['Яровое', 'Славгород', 'п', 'н']


# делаем проверку сообщения пользователя на правильность ввода
@dp.message_handler(lambda message: message.text not in x, state=FSMAdmin_Clients.Citi)
async def check_photo(message: types.Message):
    return await message.reply('Необходимо написать: Яровое или Славгород')


@dp.message_handler(state=FSMAdmin_Clients.Citi)
async def add_citi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Citi'] = message.text

    await FSMAdmin_Clients.next()
    await message.answer('Введите статус: п(проводной) или н(не проводной)')


# делаем проверку сообщения пользователя на правильность ввода
@dp.message_handler(lambda message: message.text not in x, state=FSMAdmin_Clients.Wiring)
async def check_photo(message: types.Message):
    return await message.reply('Необходимо написать: п или н!')


@dp.message_handler(state=FSMAdmin_Clients.Wiring)
async def add_wiring(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Wiring'] = message.text

    await FSMAdmin_Clients.next()
    await message.answer(f'Проверьте данные:\n'
                         f'<em>имя клиента:</em> {data["name"]}\n'
                         f'<em>номер телефона:</em> {data["Phone_number"]}\n'
                         f'<em>адрес:</em> {data["Address"]}\n'
                         f'<em>название магазина:</em> {data["Name_shop"]}\n'
                         f'<em>город:</em> {data["Citi"]}\n'
                         f'<em>статус:</em> {data["Wiring"]}'
                         f'\n'
                         f'Если всё верно нажмите "Подтвердить"')


# Клиенты - добавить - подтверждение
@dp.message_handler(commands=['Подтвердить'], state=FSMAdmin_Clients.Confirmation)
async def cmd_cancel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        list_clients = [data['Name'], data['Phone_number'], data['Address'], data['Name_shop'], data['Citi'],
                        data['Wiring']]

    # записать в bd
    result = bd.add_clients(list_clients)

    if result == True:
        await state.finish()
        await message.reply('Вы успешно добавили нового клиента!',
                            reply_markup=keyboard.kb_menu_admin())


# КЛИЕНТЫ - ИЗМЕНИТЬ
@dp.message_handler(Text(equals='Изменить 🔄 👤', ignore_case=True), state=None)
async def client_change(message: types.Message):
    await message.delete()
    await FSMAdmin_Clients_change.Id.set()

    # зайдем в bd и вытащим список клиентов с id
    list_clients = bd.id_and_name_all_clients()
    list_str_clients = ''
    for id_and_name in list_clients:
        list_str_clients = f'{list_str_clients}\n' \
                           f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Клиенты:</b>\n'
                              f'{list_str_clients}',
                         parse_mode="HTML")
    await message.answer(text='Введите id клиента:',
                         reply_markup=keyboard.get_cancel())


# МАШИНА СОСТОЯНИЙ - изменение клиента ############
@dp.message_handler(state=FSMAdmin_Clients_change.Id)
async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
        # зайдем в bd и вытащим прайс хлеба со всеми данными
        list_clients = bd.get_info_client(int(data['id']))

    # Поместим в наш словарь изначальные данные
    global CLIENTS
    CLIENTS = {'id': int(message.text), 'Name': list_clients[1], 'Phone_number': list_clients[2],
               'Address': list_clients[3], 'Name_shop': list_clients[4], 'Citi': list_clients[6],
               'Wiring': list_clients[7]}

    await message.answer(f'Наименование: {list_clients[1]}',
                         reply_markup=keyboard.get_inline_keyboard_client_change('имя'))
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('Меняем'))
async def change(callback: types.CallbackQuery):
    if callback.data == 'Меняем имя':
        await callback.message.answer(text='Введите новое имя:')
        await FSMAdmin_Clients_change.Name.set()

    if callback.data == 'Меняем телефон':
        await callback.message.answer(text='Введите новый номер:')
        await FSMAdmin_Clients_change.Phone_number.set()

    if callback.data == 'Меняем адрес':
        await callback.message.answer(text='Введите новый адрес:')
        await FSMAdmin_Clients_change.Address.set()

    if callback.data == 'Меняем название магазина':
        await callback.message.answer(text='Введите новое название:')
        await FSMAdmin_Clients_change.Name_shop.set()

    if callback.data == 'Меняем город':
        await callback.message.answer(text='Введите город:')
        await FSMAdmin_Clients_change.Citi.set()

    if callback.data == 'Меняем статус':
        await callback.message.answer(text='Введите статус:')
        await FSMAdmin_Clients_change.Wiring.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('Вперед'))
async def change(callback: types.CallbackQuery):
    if callback.data == 'Вперед имя':
        await callback.message.answer(f'Номер:  {CLIENTS["Phone_number"]}',
                                      reply_markup=keyboard.get_inline_keyboard_client_change('телефон'))

    if callback.data == 'Вперед телефон':
        await callback.message.answer(f'Адрес: {CLIENTS["Address"]}',
                                      reply_markup=keyboard.get_inline_keyboard_client_change('адрес'))

    if callback.data == 'Вперед адрес':
        await callback.message.answer(f'Название магазина: {CLIENTS["Name_shop"]}',
                                      reply_markup=keyboard.get_inline_keyboard_client_change('название магазина'))

    if callback.data == 'Вперед название магазина':
        await callback.message.answer(f'Город: {CLIENTS["Citi"]}',
                                      reply_markup=keyboard.get_inline_keyboard_client_change('город'))

    if callback.data == 'Вперед город':
        await callback.message.answer(f'Статус: {CLIENTS["Wiring"]}',
                                      reply_markup=keyboard.get_inline_keyboard_client_change('статус'))

    if callback.data == 'Вперед статус':
        await callback.message.answer(f'Проверьте данные:\n'
                                      f'<em>имя клиента:</em> {CLIENTS["Name"]}\n'
                                      f'<em>номер телефона:</em> {CLIENTS["Phone_number"]}\n'
                                      f'<em>адрес:</em> {CLIENTS["Address"]}\n'
                                      f'<em>название магазина:</em> {CLIENTS["Name_shop"]}\n'
                                      f'<em>город:</em> {CLIENTS["Citi"]}\n'
                                      f'<em>статус:</em> {CLIENTS["Wiring"]}'
                                      f'\n'
                                      f'Если всё верно нажмите "Подтвердить"')
        await FSMAdmin_Clients_change.Confirmation.set()


@dp.message_handler(state=FSMAdmin_Clients_change.Name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['Name'] = message.text

    await state.finish()
    await message.answer(f'Номер телефона: {CLIENTS["Phone_number"]}',
                         reply_markup=keyboard.get_inline_keyboard_client_change('телефон'))


@dp.message_handler(state=FSMAdmin_Clients_change.Phone_number)
async def load_photo_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['Phone_number'] = message.text
    await state.finish()
    await message.answer(f'Адрес: {CLIENTS["Address"]}\n',
                         reply_markup=keyboard.get_inline_keyboard_client_change('адрес'))


@dp.message_handler(state=FSMAdmin_Clients_change.Address)
async def load_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['Address'] = message.text

    await state.finish()
    await message.answer(f'Название магазина: {CLIENTS["Name_shop"]}\n',
                         reply_markup=keyboard.get_inline_keyboard_client_change('название магазина'))


@dp.message_handler(state=FSMAdmin_Clients_change.Name_shop)
async def load_name_shop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['Name_shop'] = message.text

    await state.finish()
    await message.answer(f'Город: {CLIENTS["Citi"]}\n',
                         reply_markup=keyboard.get_inline_keyboard_client_change('город'))


# делаем проверку сообщения пользователя на правильность ввода
@dp.message_handler(lambda message: message.text not in x, state=FSMAdmin_Clients_change.Citi)
async def check_citi(message: types.Message):
    return await message.reply('Необходимо написать: Яровое или Славгород')


@dp.message_handler(state=FSMAdmin_Clients_change.Citi)
async def add_citi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['Citi'] = message.text

    await state.finish()
    await message.answer(f'Статус: {CLIENTS["Wiring"]}\n',
                         reply_markup=keyboard.get_inline_keyboard_client_change('статус'))


# делаем проверку сообщения пользователя на правильность ввода
@dp.message_handler(lambda message: message.text not in x, state=FSMAdmin_Clients_change.Citi)
async def check_citi(message: types.Message):
    return await message.reply('Необходимо написать: "п" или "н"!!')


@dp.message_handler(state=FSMAdmin_Clients_change.Wiring)
async def add_wiring(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        CLIENTS['Wiring'] = message.text

    await state.finish()
    await message.answer(f'Проверьте данные:\n'
                         f'имя клиента: {CLIENTS["Name"]}\n'
                         f'номер телефона: {CLIENTS["Phone_number"]}\n'
                         f'адрес: {CLIENTS["Address"]}\n'
                         f'название магазина : {CLIENTS["Name_shop"]}\n'
                         f'город: {CLIENTS["Citi"]}\n'
                         f'статус: {CLIENTS["Wiring"]}'
                         f'\n'
                         f'Если всё верно нажмите "Подтвердить"')
    await FSMAdmin_Clients_change.Confirmation.set()


# Клиенты - изменить - подтверждение изменения
@dp.message_handler(commands=['Подтвердить'], state=FSMAdmin_Clients_change.Confirmation)
async def cmd_cancel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        list_clients = [CLIENTS['id'], CLIENTS['Name'], CLIENTS['Phone_number'], CLIENTS['Address'],
                        CLIENTS['Name_shop'], CLIENTS['Citi'], CLIENTS['Wiring']]

    # записать в bd
    result = bd.change_clients(list_clients)
    if result == True:
        await state.finish()
        await message.answer('Вы успешно внесли изменения клиента!',
                             reply_markup=keyboard.kb_menu_admin())


# Клиенты - УДАЛИТЬ
@dp.message_handler(Text(equals='Удалить 🚮 👤', ignore_case=True), state=None)
async def client_del(message: types.Message):
    await message.delete()
    await FSMAdmin_Clients_del.Id.set()

    # зайдем в bd и вытащим список клиентов с id
    list_clients = bd.id_and_name_all_clients()
    list_str_clients = ''
    for id_and_name in list_clients:
        list_str_clients = f'{list_str_clients}\n' \
                           f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Клиенты:</b>\n'
                              f'{list_str_clients}',
                         parse_mode="HTML")
    await message.answer(text='Введите id клиента:',
                         reply_markup=keyboard.get_cancel())


# Клиенты - УДАЛИТЬ - клиента
@dp.message_handler(state=FSMAdmin_Clients_del.Id)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    # из bd вытащим данные клиента и поместим в список
    client = bd.get_info_client(data['id'])

    await FSMAdmin_Clients_del.next()
    await message.answer(f'Вы хотите удалить клиента: {client[1]}')
    await message.answer(f'Если всё верно нажмите "Подтвердить"')


# Клиенты - удалить - подтверждение удаления
@dp.message_handler(commands=['Подтвердить'], state=FSMAdmin_Clients_del.Confirmation)
async def cmd_cancel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # из bd вытащим данные клиента и поместим в список
        client = bd.get_info_client(data['id'])
        # удаляем из bd
        result = bd.del_clients(data['id'])

    if result == True:
        await state.finish()
        await message.answer(f'Вы успешно удалили клиента {client[1]}!',
                             reply_markup=keyboard.kb_menu_admin())


# Клиенты - удалить - выход из машины состояний
@dp.message_handler(commands=['cancel'], state='*')  # если нажали cancel в любом из состаяний
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state == None:
        return

    await state.finish()
    await message.reply('Вы прервали ввод данных!',
                        reply_markup=keyboard.kb_menu_admin())

    # очистим словарь
    BROD.clear()


########################################################################################################################


# menu 'Хлеб'
@dp.message_handler(Text(equals='Хлеб 🍞'))
async def admin_application(message: types.Message):
    await message.delete()
    await message.answer(text='Вы зашли в меню "Хлеб"',
                         reply_markup=keyboard.kb_menu_brod_admin())


# menu 'Хлеб'- Добавить
@dp.message_handler(Text(equals='Добавить + 🍞'))
async def brod_add(message: types.Message):
    await FSMAdmin_Brod_add.Name.set()
    await message.answer('Напишите название хлеба например - Хлеб Степной',
                         reply_markup=keyboard.get_cancel())


@dp.message_handler(state=FSMAdmin_Brod_add.Name)
async def load_brod_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await FSMAdmin_Brod_add.next()
    await message.reply('Запишите вес хлеба в граммах например: 500')


@dp.message_handler(state=FSMAdmin_Brod_add.Heft)
async def load_brod_heft(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['heft'] = message.text
    await FSMAdmin_Brod_add.next()
    await message.reply('А теперь добавьте цену хлеба для Ярового, например: 40')


@dp.message_handler(state=FSMAdmin_Brod_add.Price_jr)
async def load_brod_price_jr(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_jr'] = message.text
    await FSMAdmin_Brod_add.next()
    await message.reply('И цену хлеба для Славгорода, например: 41')


@dp.message_handler(state=FSMAdmin_Brod_add.Price_sl)
async def load_brod_price_sl(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_sl'] = message.text

    await FSMAdmin_Brod_add.next()
    await message.reply('А теперь добавьте фото хлеба:')


@dp.message_handler(lambda message: not message.photo, state=FSMAdmin_Brod_add.Photo)
async def check_photo(message: types.Message):
    return await message.reply('это не фото')


@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=FSMAdmin_Brod_add.Photo)
async def load_brod_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await FSMAdmin_Brod_add.next()
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=data['photo'],
                         caption=f'Название: {data["name"]}\n'
                                 f'Вес: {data["heft"]}\n'
                                 f'Цена для Ярового: {data["price_jr"]}\n'
                                 f'Цена для Славгорода: {data["price_sl"]}\n')
    await message.answer(text='Если всё верно нажмите "Подтвердить"')


@dp.message_handler(commands=['Подтвердить'], state=FSMAdmin_Brod_add.Confirmation)
async def cmd_cancel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        list_data_brod_add = [data["name"], data["heft"], data["price_jr"], data["price_sl"], data["photo"]]
        # запишем новый хлеб в базу данных=
        result = bd.add_brod(list_data_brod_add)

    if result == True:
        await message.answer(f'Вы успешно добавили {data["name"]} в базу данных!',
                             reply_markup=keyboard.kb_menu_admin())
        await state.finish()


# menu 'Хлеб'- Изменить

# создадим переменную и будем помещать в неё новуб информацию о хлебе
BROD = {}


@dp.message_handler(Text(equals='Изменить 🍞🔄🥖'))
async def brod_add(message: types.Message):
    await FSMAdmin_Brod_change.ID.set()
    # await message.answer('Напишите название хлеба например - Хлеб Степной',
    #                      reply_markup=keyboard.get_cancel())
    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()
    # сделаем в удобном формате строку с данными по хлебу(id-наименование)
    list_str_brod = ''
    for id_and_name in list_brod:
        list_str_brod = f'{list_str_brod}\n' \
                        f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Прайс:</b>\n'
                              f'{list_str_brod}',
                         parse_mode="HTML")
    await message.answer(text='Введите необходимый id :',
                         reply_markup=keyboard.get_cancel())


@dp.message_handler(state=FSMAdmin_Brod_change.ID)
async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = int(message.text)
        # зайдем в bd и вытащим прайс хлеба со всеми данными
        list_brod = bd.price_brod()

        list_brod_change = []
        # Вытащим нужный нам хлеб с данными по id и поместим в список
        for brod in list_brod:
            if brod[0] == data['id']:
                for brod_data in brod:
                    list_brod_change.append(brod_data)

    # Поместим в наш словарь изначальные данные
    global BROD
    BROD = {'id': message.text, 'name': list_brod_change[1], 'heft': list_brod_change[2],
            'price_jr': list_brod_change[3], 'price_sl': list_brod_change[4], 'photo': list_brod_change[5]}

    await message.answer(f'Наименование: 🥨{list_brod_change[1]}🥨',
                         reply_markup=keyboard.get_inline_keyboard_brod_change3('наименование'))
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('Измен'))
async def change(callback: types.CallbackQuery):
    if callback.data == 'Изменить наименование':
        await callback.message.answer(text='Введите новое имя:')
        await FSMAdmin_Brod_change.Name.set()

    if callback.data == 'Изменить вес':
        await callback.message.answer(text='Введите новое вес:')
        await FSMAdmin_Brod_change.Heft.set()

    if callback.data == 'Изменить Цена Яровое':
        await callback.message.answer(text='Введите новую цену:')
        await FSMAdmin_Brod_change.Price_jr.set()

    if callback.data == 'Изменить Цена Славгород':
        await callback.message.answer(text='Введите новую цену:')
        await FSMAdmin_Brod_change.Price_sl.set()

    if callback.data == 'Изменить Фото':
        await callback.message.answer(text='Добавьте новое фото:')
        await FSMAdmin_Brod_change.Photo.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('Дальше'))
async def change(callback: types.CallbackQuery):
    if callback.data == 'Дальше наименование':
        await callback.message.answer(f'Вес: ⚖️ {BROD["heft"]}',
                                      reply_markup=keyboard.get_inline_keyboard_brod_change3('вес'))

    if callback.data == 'Дальше вес':
        await callback.message.answer(f'Цена Яровое: {BROD["price_jr"]}',
                                      reply_markup=keyboard.get_inline_keyboard_brod_change3('Цена Яровое'))

    if callback.data == 'Дальше Цена Яровое':
        await callback.message.answer(f'Цена Славгород: {BROD["price_sl"]}',
                                      reply_markup=keyboard.get_inline_keyboard_brod_change3('Цена Славгород'))

    if callback.data == 'Дальше Цена Славгород':

        if BROD['photo'] == None:
            # await callback.message.answer(f'Фото: \n'
            #                               f'{BROD["photo"]}',
            #                               reply_markup=keyboard.get_inline_keyboard_brod_change3('Фото'))

            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=BROD['photo'],
                                 reply_markup=keyboard.get_inline_keyboard_brod_change3('Фото'))
        else:
            await callback.message.answer(f'Фото нет!',
                                          reply_markup=keyboard.get_inline_keyboard_brod_change3('Фото'))


@dp.message_handler(state=FSMAdmin_Brod_change.Name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        BROD['name'] = message.text

    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()

    await state.finish()

    await message.answer(f'Вес: ⚖️{BROD["heft"]}⚖️',
                         reply_markup=keyboard.get_inline_keyboard_brod_change3('вес'))

    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷📧✉️


@dp.message_handler(state=FSMAdmin_Brod_change.Heft)
async def load_heft(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        BROD['heft'] = message.text

    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()

    await state.finish()

    await message.answer(f'Цена Яровое: {BROD["price_jr"]}',
                         reply_markup=keyboard.get_inline_keyboard_brod_change3('Цена Яровое'))


@dp.message_handler(state=FSMAdmin_Brod_change.Price_jr)
async def load_heft(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        BROD['price_jr'] = message.text

    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()

    await state.finish()

    await message.answer(f'Цена Славгород: {BROD["price_sl"]}',
                         reply_markup=keyboard.get_inline_keyboard_brod_change3('Цена Славгород'))


@dp.message_handler(state=FSMAdmin_Brod_change.Price_sl)
async def load_heft(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        BROD['price_sl'] = message.text

    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()

    await state.finish()

    await message.answer(f'Фото: \n'
                         f'{BROD["photo"]}',
                         reply_markup=keyboard.get_inline_keyboard_brod_change3('Фото'))
    await message.answer(text='Если всё верно нажмите "Подтвердить"')


@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=FSMAdmin_Brod_change.Photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        BROD['photo'] = message.photo[0].file_id

    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()

    await FSMAdmin_Brod_change.next()

    await bot.send_photo(chat_id=message.from_user.id,
                         photo=BROD['photo'],
                         caption=f'Название: {BROD["name"]}\n'
                                 f'Вес: {BROD["heft"]}\n'
                                 f'Цена для Ярового: {BROD["price_jr"]}\n'
                                 f'Цена для Славгорода: {BROD["price_sl"]}\n')
    await message.answer(text='Если всё верно нажмите "Подтвердить"')


@dp.message_handler(commands=['Подтвердить'], state=FSMAdmin_Brod_change.Confirmation)
async def cmd_cancel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        list_data_brod_change = [BROD["id"], BROD["name"], BROD["heft"], BROD["price_jr"], BROD["price_sl"],
                                 BROD["photo"]]

        # запишем изменения в базу данных
        result = bd.change_brod(list_data_brod_change)

    if result == True:
        await message.answer('Успешно!',
                             reply_markup=keyboard.kb_menu_admin())
        await state.finish()

    # очистим словарь
    BROD.clear()


# Хлеб - УДАЛИТЬ
@dp.message_handler(Text(equals='Удалить - 🗑'))
async def brod_add(message: types.Message):
    await FSMAdmin_Brod_del.ID.set()
    await message.answer('Список хлеба:',
                         reply_markup=keyboard.get_cancel())
    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()
    # сделаем в удобном формате строку с данными по хлебу(id-наименование)
    list_str_brod = ''
    for id_and_name in list_brod:
        list_str_brod = f'{list_str_brod}\n' \
                        f'id: <em>{id_and_name[0]}</em> - имя: <em>{id_and_name[1]}</em> '
    # выведем получившейся список
    await message.answer(text=f'<b>Прайс:</b>\n'
                              f'{list_str_brod}',
                         parse_mode="HTML")
    await message.answer(text='Введите необходимый id :',
                         reply_markup=keyboard.get_cancel())


# ловим ID для удаления хлеба
@dp.message_handler(state=FSMAdmin_Brod_del.ID)
async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        BROD['id'] = int(message.text)
    await FSMAdmin_Brod_del.next()

    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()

    list_brod_del = []

    for data_brod in list_brod:
        if data_brod[0] == BROD['id']:
            for da in data_brod:
                list_brod_del.append(da)

    await message.reply(text=f'Если вы хотите удалить: {list_brod_del[1]}\n'
                             f'нажмите "Подтвердить" ')


@dp.message_handler(commands=['Подтвердить'], state=FSMAdmin_Brod_del.Confirmation)
async def cmd_cancel(message: types.Message, state: FSMContext):
    # зайдем в bd и вытащим прайс хлеба со всеми данными
    list_brod = bd.price_brod()

    list_brod_del = []

    for data_brod in list_brod:
        if data_brod[0] == BROD['id']:
            for da in data_brod:
                list_brod_del.append(da)

    # Удалим хлеб из bd по id
    result = bd.del_brod(BROD['id'])
    if result == True:
        await message.answer(f'Наименование: 🥨{list_brod_del[1]}\n'
                             f'было успешно удалено!',
                             reply_markup=keyboard.kb_menu_admin())

    await state.finish()

    # очистим словарь
    BROD.clear()


# menu '<< Назад'
@dp.message_handler(Text(equals='<< Назад'))
async def admin_application(message: types.Message):
    await message.delete()
    await message.answer(text='Вы зашли в основное меню',
                         reply_markup=keyboard.kb_menu_admin())


# menu 'Итог(распечатка рассылка)
@dp.message_handler(Text(equals='Итог(распечатка рассылка)'))
async def finish(message: types.Message):
    await message.delete()

    # поместим все постоянные заявки в основную заявку
    bd.add_permanent_app()

    # ЯРОВОЕ

    # зайдем в bd и поместим в список клиентов Яровских и выведим итог
    list_app_jr_pr = bd.app_jr_pr(list_name_brod2_osnov)

    # создаём принтер через модуль PrintList
    app = QtWidgets.QApplication(sys.argv)
    pl = PrintList.PrintList()

    # добавляем строки из нашего списка заявок
    pl.data = list_app_jr_pr

    # програмируем ширину столбцов
    pl.columnWidths = [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
                       30, 30, 30, 30, 30, 30, 30, 30, 30]

    # добавляем имена колонок
    pl.headers = list_name_brod2_osnov_print

    # запускаем поринтер
    pl.printData()

    # СЛАВГОРОД

    # зайдем в bd и поместим в список клиентов Славгорода и выведим итог
    list_app_sl = bd.app_sl(list_name_brod2_osnov)

    # создаём принтер через модуль PrintList
    app = QtWidgets.QApplication(sys.argv)
    pl = PrintList.PrintList()
    # # добавляем строки из нашешго списка заявок
    pl.data = list_app_sl
    # программируем ширину столбцов
    pl.columnWidths = [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
                       30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

    # добавляем имена колонок
    pl.headers = list_name_brod2_osnov_print
    # запускаем принтер
    pl.printData()

    # создаём печатный документ для Галины Васильевны_____________________________________________________________
    list_val_dop_app = bd.app_dop(list_name_brod2_dop)

    # создаём принтер через модуль PrintList
    app = QtWidgets.QApplication(sys.argv)
    pl = PrintList.PrintList()
    # # добавляем строки из нашешго списка заявок
    pl.data = list_val_dop_app
    # # програмируем ширину столбцов
    pl.columnWidths = [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    # # добавляем имена колонок
    pl.headers = list_name_brod2_dop_print
    # запускаем поринтер
    pl.printData()

    await message.answer(text='Успешно',
                         reply_markup=keyboard.kb_menu_admin())


########################################################################################################################


########################################################################################################################


########################################################################################################################

# РЕГИСТРАЦИЯ КЛИЕНТА
########################################################################################################################
# этот хендлер обрабатывает только фразу 'Зарегистрироваться'
@dp.message_handler(Text(equals='Зарегистрироваться'))
async def reg(message: types.Message):
    await message.delete()
    await message.answer(text='Введите ваш номер для регистрации')


# хендлер РЕГИСТРАЦИИ КЛИЕНТА ловящий его CliensID и записывающий в таблицу его ID устройства
@dp.message_handler(Text(equals=range(1, 49)))
async def reg(message: types.Message):
    result_registration = bd.registration_clients(message.from_user.id, message.text)
    if result_registration:
        await message.answer(text='Вы успешно зарегистрировались\n'
                                  'теперь можете делать заявки',
                             reply_markup=keyboard.kb_menu())


########################################################################################################################


# начальный распределительный хендлер
########################################################################################################################
@dp.message_handler()
async def start_command(message: types.Message):
    # для начала зайдем в базу данных скачаем ID2 клиентов и список
    id_clientse = bd.list_id2_clients()

    # если клиент не зарегистрирован, то откроем клавиатуру для регистрации
    if message.from_user.id not in id_clientse:
        await bot.send_message(chat_id=message.from_user.id,  # отписываемся в личный чат
                               text='Необходимо зарегистрироваться',  # пишем этот текст
                               reply_markup=keyboard.kb_reg())  # запускаем клавиатуру
        await message.delete()

    # если вы админ откроем админское меню
    elif message.from_user.id == ADMIN:
        await bot.send_message(chat_id=message.from_user.id,  # отписываемся в личный чат
                               text='Привет Наташа',  # пишем этот текст
                               reply_markup=keyboard.kb_menu_admin())  # запускаем клавиатуру
        await message.delete()

    # если клиент зарегистрирован, то откроем клавиатуру клиентская
    else:
        await bot.send_message(chat_id=message.from_user.id,  # отписываемся в личный чат
                               text=hi_text,  # пишем этот текст
                               reply_markup=keyboard.kb_menu())  # запускаем клавиатуру
        await message.delete()


########################################################################################################################


if __name__ == '__main__':
    # dp.middleware.setup(CustomMiddleware())
    executor.start_polling(skip_updates=True,  # при включении бота он не будет отвечать на старые сообщения
                           dispatcher=dp,  # запускаем деспетчер
                           on_startup=on_startup)  # запускаем функцию, информирующую о запуске бота
