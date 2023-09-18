from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton



ikb = InlineKeyboardMarkup(row_width=2)
bat1 = InlineKeyboardButton(text='Button 1',
                            url='https://www.youtube.com/watch?v=qivjEiONPy4'
                            )
bat2 = InlineKeyboardButton(text='Button 2',
                            url='https://www.youtube.com/watch?v=qivjEiONPy4')

ikb.add(bat1)
ikb.insert(bat2)