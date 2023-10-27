from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton


# 🗓✏️📝🖌🖍📌🖇📎🧮🔎🔍🔄➡️⬅️⬆️⬇️↩️💬💭🗯🚮⚛️🆔
# 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷
# 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷📧✉️🧹⚖️

# КЛИЕНТСКАЯ
########################################################################################################################

# РЕГИСТРАЦИЯ КЛИЕНТА
def kb_reg():
    kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)
    # )# создали клавиатуру,
    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)

    kb_reg.add(KeyboardButton('Зарегистрироваться'))  # cоздали кнопку

    return kb_reg


# ГЛАВНОЕ МЕНЮ
def kb_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)#resize_keyboard=True,
                             #row_width=5,
    # )# создали клавиатуру,
    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)

    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷
    kb.add(KeyboardButton('Сделать  🍞/ изменить заявку'))  # cоздали кнопку
    kb.add(KeyboardButton('Удалить заявку'))  # cоздали кнопку
    kb.add(KeyboardButton('Прайс-Яровое 🥨'), KeyboardButton('Прайс-Славгород 🍪'))
    kb.add(KeyboardButton('Прайс с Фото 📷 (Яровое, Славгород)'))
    kb.add(KeyboardButton('Контакты ☎️'), KeyboardButton('Вакансии 👤'))
    kb.add(KeyboardButton('Оставить отзыв и предложения 💌'))

    return kb


# Клиент - инлайн клавиатура +,-,= к заявке
def get_iline_keyboard(ind_lis, result) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=5, inline_keyboard=[
        [InlineKeyboardButton('-', callback_data=f'-{ind_lis}'),
         InlineKeyboardButton('+', callback_data=f'+{ind_lis}'),
         InlineKeyboardButton(f'= {result} шт.', callback_data=f'{result}')],
        [InlineKeyboardButton('-10', callback_data=f'10-{ind_lis}'),
         InlineKeyboardButton('+10', callback_data=f'10+{ind_lis}')]
    ])

    return ikb


# Клиент - клавиатура с кнопками "назад(в меню клиента), корзина, подтвердить"
def back_cart_confirm():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)  # создали клавиатуру,

    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)
    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪💰⬅️
    kb.add(KeyboardButton('⬅️Назад'), KeyboardButton('Корзина 🛒'), KeyboardButton('Подтвердить 💰'))  # cоздали кнопки

    return kb


# Клиент - инлайн кноки да, нет посмотреть старую заявку
def get_iline_keyboard_yes_no_look() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [InlineKeyboardButton('Да', callback_data='!Да'),
         InlineKeyboardButton('Нет', callback_data='!Нет')],
        [InlineKeyboardButton('Открыть старую заявку', callback_data='!Старая заявка')]
    ])

    return ikb


# Клиент - инлайн кноки да, нет на вопрос 'переписать заявку'
def get_iline_keyboard_yes_no() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [InlineKeyboardButton('Да', callback_data='!Да'),
         InlineKeyboardButton('Нет', callback_data='!Нет')],
    ])

    return ikb


########################################################################################################################


# АДМИНСКАЯ
########################################################################################################################

# ГЛАВНОЕ МЕНЮ
def kb_menu_admin():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # )# создали клавиатуру,
    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)

    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷
    kb.add(KeyboardButton('Заявки ✉️'))
    kb.add(KeyboardButton('Постоянные заявки 📧'))
    kb.add(KeyboardButton('Клиенты 👤'))
    kb.add(KeyboardButton('Хлеб 🍞'))
    kb.add(KeyboardButton('Итог(распечатка рассылка)'))


    return kb


# ЗАЯВКИ
def kb_menu_application_admin():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # )# создали клавиатуру,
    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)

    kb.add(KeyboardButton('Добавить + 📝, Изменить 🔄'))
    kb.add(KeyboardButton('Удалить 🗑'))
    kb.add(KeyboardButton('<< Назад'))

    return kb


# Заявки - "назад(в меню админа), корзина, подтвердить"
def back_cart_confirm_admin():
    # ✍️🗑‼️⁉️❗️🔙
    kb = ReplyKeyboardMarkup(resize_keyboard=True)  # создали клавиатуру,

    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)
    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪💰⬅️
    kb.add(KeyboardButton('🔙Назад'), KeyboardButton('Корзина 🗑'), KeyboardButton('Подтвердить ✍️'))  # cоздали кнопки

    return kb


# Заявки - да, нет посмотреть заявку для АДМИНА
def get_inline_keyboard_yes_no_look_admin() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [InlineKeyboardButton('Да', callback_data='?Да'),
         InlineKeyboardButton('Нет', callback_data='?Нет')],
        [InlineKeyboardButton('Открыть старую заявку', callback_data='?Старая заявка')]
    ])

    return ikb


# Заявки - да, нет на вопрос 'переписать заявку' для АДМИНА
def get_iline_keyboard_yes_no_admin() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [InlineKeyboardButton('Да', callback_data='?Да'),
         InlineKeyboardButton('Нет', callback_data='?Нет')],
    ])

    return ikb


# ПОСТОЯННЫЕ ЗАЯВКИ
def kb_menu_constant_application_admin():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # )# создали клавиатуру,
    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)
    # 🗓✏️📝🖌🖍📌🖇📎🧮🔎🔍🔄➡️⬅️⬆️⬇️↩️💬💭🗯🚮⚛️🆔
    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷
    kb.add(KeyboardButton('Добавить 🖌, Изменить 🔄'))
    kb.add(KeyboardButton('Удалить 🚮'))
    kb.add(KeyboardButton('<< Назад'))

    return kb


# Постоянные заявки - инлайн клавиатура дни недели для ДОБАВЛЕНИЯ и УДАЛЕНИЯ(в зависимости от action)
def get_inline_keyboard_deys_of_week(action):
    ikb = InlineKeyboardMarkup(row_width=3,
                               inline_keyboard=[
                                   [InlineKeyboardButton('Понедельник', callback_data=f'{action}Понедельник'),
                                    InlineKeyboardButton('Вторник', callback_data=f'{action}Вторник')],
                                   [InlineKeyboardButton('Среда', callback_data=f'{action}Среда'),
                                    InlineKeyboardButton('Четверг', callback_data=f'{action}Четверг')],
                                   [InlineKeyboardButton('Пятница', callback_data=f'{action}Пятница'),
                                    InlineKeyboardButton('Суббота', callback_data=f'{action}Суббота')]
                               ])

    return ikb


# Подтвердить постоянную заявку
def confirm_applications():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷
    kb.add(KeyboardButton('Подтвердить!'))
    kb.add(KeyboardButton('<< Назад'))
    return kb


# КЛИЕНТЫ
def kb_menu_clients_admin():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # )# создали клавиатуру,
    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)

    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷
    kb.add(KeyboardButton('Добавить + 👤'))
    kb.add(KeyboardButton('Изменить 🔄 👤'))
    kb.add(KeyboardButton('Удалить 🚮 👤'))
    kb.add(KeyboardButton('<< Назад'))

    return kb


# клавиатура для подтверхдения добавления нового клиента
def get_cancel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/Подтвердить'))
    kb.add(KeyboardButton('/cancel'))

    return kb


# ХЛЕБ
def kb_menu_brod_admin():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # )# создали клавиатуру,
    # вписывающейся в интерфейс(resize_keyboard=True),
    # и самозакрывается (one_time_keyboard=True)

    # 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷
    kb.add(KeyboardButton('Добавить + 🍞'))
    kb.add(KeyboardButton('Изменить 🍞🔄🥖'))
    kb.add(KeyboardButton('Удалить - 🗑'))
    kb.add(KeyboardButton('<< Назад'))

    return kb



# инлайн клавиатура для изменения данных хлеба
def get_inline_keyboard_brod_change(name, heft, price_jr, price_sl):
    ikb = InlineKeyboardMarkup(row_width=3,
                               inline_keyboard=[
                                   [InlineKeyboardButton('Имя:', callback_data=f'q'),
                                    InlineKeyboardButton(f'{name}', callback_data=f'q'),
                                    InlineKeyboardButton(f'Изменить имя', callback_data=f'Изменить имя')],

                                   [InlineKeyboardButton('Вес:', callback_data=f'q'),
                                    InlineKeyboardButton(f'{heft}', callback_data=f'q'),
                                    InlineKeyboardButton(f'Изменить вес', callback_data=f'Изменить вес')],

                                   [InlineKeyboardButton('Цена Яровое:', callback_data=f'q'),
                                    InlineKeyboardButton(f'{price_jr}', callback_data=f'q'),
                                    InlineKeyboardButton(f'Изменить цену', callback_data=f'Изменить цену Яровое')]
                                   ,
                                   [InlineKeyboardButton('Цена Славгород:', callback_data=f'q'),
                                    InlineKeyboardButton(f'{price_sl}', callback_data=f'q'),
                                    InlineKeyboardButton(f'Изменить цену', callback_data=f'Изменить цену Славгород')],
                               ])

    return ikb


def get_inline_keyboard_brod_change2(what, data):
    ikb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [InlineKeyboardButton(f'{what}:', callback_data=f'q'),
                                    InlineKeyboardButton(f'{data}', callback_data=f'q')],

                                   [InlineKeyboardButton(f'Изменить {what}', callback_data=f'Изменить {what}'),
                                    InlineKeyboardButton(f'Дальше', callback_data=f'Дальше')]
                               ])

    return ikb


def get_inline_keyboard_brod_change3(what):
    ikb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [InlineKeyboardButton('Изменить', callback_data=f'Изменить {what}'),
                                    InlineKeyboardButton('Дальше', callback_data=f'Дальше {what}')]
                                               ]
                               )


    return ikb

# клиент клава изменить- дальше
def get_inline_keyboard_client_change(what):
    ikb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [InlineKeyboardButton('Изменить', callback_data=f'Меняем {what}'),
                                    InlineKeyboardButton('Дальше', callback_data=f'Вперед {what}')]
                                               ]
                               )


    return ikb
# 🥖 🥐🥯🍞🥨🌭🍔🥪🍩🍪☎️💸🛒🗑💌👤📷📧✉️🧹⚖️