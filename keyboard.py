from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


main_kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True,selective=True
                              )
button_dice = KeyboardButton(text='dice')
button_test = KeyboardButton(text ="Еще не придумал")
button_tes = KeyboardButton(text ="Еще не придуапрпарпарпамал")

main_kb.add(button_dice).add(button_test).add(button_tes)
