from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
kb = ReplyKeyboardMarkup(resize_keyboard=True)
bp1 = KeyboardButton("Random")
bp2 = KeyboardButton("Menu")
kb.add(bp1,bp2)

IKB = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text="Like",
                           callback_data="like")
ib2 = InlineKeyboardButton(text="Dislike",
                           callback_data="Dislike")
ib3 = InlineKeyboardButton(text="Next Photo",
                           callback_data="Next")
IKB.add(ib1,ib2).add(ib3)
