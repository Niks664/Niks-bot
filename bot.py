import config
import logging
from aiogram import Bot,Dispatcher,types, executor
from filters import IsAdminFilter
from db import Database
import keyboard
from asyncio import sleep

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
kd = Dispatcher(bot)
db = Database('database.db')

kd.filters_factory.bind(IsAdminFilter)

@kd.message_handler(commands= ["games"], commands_prefix="!/")
async def game(message: types.Message):
    await message.reply(text= f'@{message.from_user.username} Во что хочешь поиграть?',
                        reply_markup = keyboard.main_kb)
    
@kd.message_handler(text = "dice")
async def dice(message: types.Message):
    ab = await message.bot.send_dice(chat_id = config.GROUP_ID) 
    dice = ab['dice']["value"]
    await sleep(4)
    print(dice)
    if dice > 3:
        await message.reply (f"Поздравляю @{message.from_user.username} ты победил! И получил 100 $.")
        balanceadd = 100
        db.add_balance(message.from_user.id, balanceadd)
        balances = db.get_balance(message.from_user.id)
        await message.reply(f"Баланс @{message.from_user.username} успешно пополнен на {balanceadd} $\nБаланс пользователя: {balances} $ ")
    else:
        await sleep(4)
        await message.reply (f" @{message.from_user.username} Увы, но ты неудачник! :(")
    
@kd.message_handler(is_admin=True, commands = ["mute"], commands_prefix = '!/')
async def cmd_mute(message: types.Message):
    logging.info(f'Entry cmd_mute: {message.from_id=} { message.text=}')
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return
    mute_min = int(message.text[6:])
    db.add_mute(message.reply_to_message.from_user.id, mute_min)
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.reply_to_message.reply(f"Пользователь был замучен на {mute_min} минут! \nПомолчи пж :)")
    
@kd.message_handler(is_admin=True, commands = ["unmute"], commands_prefix = '!/')
async def cmd_unmute(message: types.Message):
    logging.info(f'Entry cmd_unmute: {message.from_id=} { message.text=}')
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return
    db.un_mute(message.reply_to_message.from_user.id)
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.reply_to_message.reply(f"Пользователь был размучен! \nПоговори пж :)")

@kd.message_handler(is_admin=True, commands = ["ban"], commands_prefix = '!/')
async def cmd_ban(message: types.Message):
    logging.info(f'Entry cmd_ban: {message.from_id=} { message.text=}')
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return

    await message.bot.kick_chat_member(chat_id = config.GROUP_ID, user_id = message.reply_to_message.from_user.id)
    await message.reply_to_message.reply("Пользователь забанен! \nТуда малышку :)")

@kd.message_handler(commands = ["balance"], commands_prefix = '!/')
async def cmd_balance(message: types.Message):
    balances = db.get_balance(message.from_user.id)
    await message.reply(f"Ваш баланс: {balances} $ ")
    
@kd.message_handler(is_admin=True,commands = ['addbalance'], commands_prefix = '!/')
async def cmd_addbalance(message: types.Message):
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return
    balanceadd = int(message.text[11:])
    db.add_balance(message.reply_to_message.from_user.id, balanceadd)
    balances = db.get_balance(message.reply_to_message.from_user.id)
    await message.reply_to_message.reply(f"Баланс @{message.reply_to_message.from_user.username} успешно пополнен на {balanceadd} $\nБаланс пользователя: {balances} $ ")
    
@kd.message_handler(is_admin=True,commands = ['removebalance'], commands_prefix = '!/')
async def cmd_removebalance(message: types.Message):
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return
    balancremove = int(message.text[14:])
    db.remove_balance(message.reply_to_message.from_user.id, balancremove)
    balances = db.get_balance(message.reply_to_message.from_user.id)
    await message.reply_to_message.reply(f"Баланс пользователя успешно удален на {balancremove} $\nБаланс пользователя: {balances} $ ")

# @kd.message_handler(commands = ["leaders"], commands_prefix = '!/')
# async def cmd_leaders(message: types.Message):
#     leaders = db.get_leaderboard()
#     await message.reply(f"Лидеры: {leaders}")

@kd.message_handler(commands = ['help'], commands_prefix = '!/')
async def start_command(message: types.Message):
    user_username = message.from_user.username
    await message.reply(f"@{user_username} Помощь по коммандам:\n \nКоманды для модерации:\n\n!mute - Замутить человека на определенное время, используется ответом на сообщение.\n\n!unmute - Снять мут с пользователя, используется ответом на сообщение.\n\n!ban - Забанить пользователя на всегда, используется ответом на сообщение.\n\n!addbalance - Пополнить баланс пользователю, используется ответом на сообщение.\n\n!removebalance - Испольльзуется чтобы понизить баланс пользователю, используется ответом на сообщение.\n\nКоманды для пользователей:\n\n!balance - Узнать свой баланс. ")

@kd.message_handler(commands = "stats", commands_prefix = "!/")
async def start(message: types.Message):
    balances = db.get_balance(message.from_user.id)
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    # print(member)
    status = member['status']
    # print(status)
    status_player = 'Пользователь'
    status_admin = 'Администратор'
    if status == 'member':
        await message.reply(f'Username: @{message.from_user.username}\nUserid: {message.from_user.id}\nБаланс: {balances}\nСтатус: {status_player}')
    else:
        await message.reply(f'Username: @{message.from_user.username}\nUserid: {message.from_user.id}\nБаланс: {balances}\nСтатус: {status_admin}')

# @kd.message_handler(commands="hello", commands_prefix="!/")
# async def send_hello(message: types.Message):
#     your_id = message.from_id
#     your_name = message.from_user.username
#     try:
#         friend_name = message.reply_to_message.from_user.username
#         friend_id = message.reply_to_message.from_user.id
#         # await message.delete()
#         await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) пожал руку [{friend_name}](tg://user?id={str(friend_id)})', parse_mode="Markdown")
#     except:
#         # await message.delete()
#         await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) жмет руку всем', parse_mode="Markdown")





@kd.message_handler()
async def process_message(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    db.add_usernames(message.from_user.username, message.from_user.id)
    # if not db.mute(message.from_user.id):
    #     print("/")
    # else:
    #     await message.delete()
        
      
@kd.message_handler()
async def filter_messages(message: types.Message):
    logging.info(f'Entry filter_messages: {message.from_id=} { message.text=}')
    if "Проверка" in message.text:
        await message.delete()
    # if not db.mute(message.from_user.id):
    #     print("/")
    # else:
    #     await message.delete()


if __name__ == "__main__":
    print("Starting...", end='')
    executor.start_polling(kd, skip_updates=True)