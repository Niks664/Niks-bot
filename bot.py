import config
import logging
from aiogram import Bot,Dispatcher,types, executor
from filters import IsAdminFilter
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
kd = Dispatcher(bot)
db = Database('database.db')

kd.filters_factory.bind(IsAdminFilter)

@kd.message_handler(is_admin=True, commands = ["mute"], commands_prefix = '!/')
async def cmd_mute(message: types.Message):
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return
    mute_min = int(message.text[6:])
    db.add_mute(message.reply_to_message.from_user.id, mute_min)
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.reply_to_message.reply(f"Пользователь был замучен на {mute_min} секунд! \nПомолчи пж :)")
    
@kd.message_handler(is_admin=True, commands = ["ban"], commands_prefix = '!/')
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return

    await message.bot.kick_chat_member(chat_id = config.GROUP_ID, user_id = message.reply_to_message.from_user.id)
    await message.reply_to_message.reply("Пользователь забанен! \nТуда малышку :)")

@kd.message_handler(commands = ['help'], commands_prefix = '!/') 
async def start_command(message: types.Message):
    await message.reply("Привет! \nСкоро тут будет инфа :)")
    
        
@kd.message_handler()
async def filter_messages(message: types.Message):    
    if "Проверка" in message.text:
        await message.delete()
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    if not db.mute(message.from_user.id):
        print("/")
    else:
        await message.delete()

if __name__ == "__main__":
    executor.start_polling(kd, skip_updates=True)