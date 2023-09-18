from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         row_width=1)
b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/start')
b3 = KeyboardButton(text='/description')
b4 = KeyboardButton(text='Random photo')
b5 = KeyboardButton(text='/lacation')
kb.add(b1, b2, b3, b4, b5)

kb2 = ReplyKeyboardMarkup(resize_keyboard=True,
                         row_width=1)
ba1 = KeyboardButton(text='Random')
ba2 = KeyboardButton(text='Menu')

kb2.add(ba1, ba2)

ikb = InlineKeyboardMarkup(row_width=2)
ibat1 = InlineKeyboardButton(text='Следующее фото',
                            callback_data='next'
                            )
ibat2 = InlineKeyboardButton(text='Нравится',
                             callback_data='like'
                            )
ibat3 = InlineKeyboardButton(text='Не нравится',
                             callback_data='dislike'
                            )
ibat4 = InlineKeyboardButton(text='Главное меню',
                            callback_data='Menu'

                            )
ibat5 = InlineKeyboardButton(text='Menu',
                             callback_data='menu')
ikb.add(ibat1)
ikb.add(ibat2)
ikb.insert(ibat3)
ikb.add(ibat4)
ikb.add(ibat5)


