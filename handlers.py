
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

@kd.message_handler(is_admin=True,commands = ['addbalance'], commands_prefix = '!/')
async def cmd_addbalance(message: types.Message):
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return
    balanceadd = int(message.text[11:])
    db.add_balance(message.reply_to_message.from_user.id, balanceadd)
    balances = db.get_balance(message.reply_to_message.from_user.id)
    await message.reply_to_message.reply(f"Баланс пользователя успешно пополнен на {balanceadd} $\nБаланс пользователя: {balances} $ ")
    
@kd.message_handler(is_admin=True,commands = ['removebalance'], commands_prefix = '!/')
async def cmd_removebalance(message: types.Message):
    if not message.reply_to_message:
        await message.reply ("Эта команда должна быть ответом на сообщение!")
        return
    balancremove = int(message.text[14:])
    db.remove_balance(message.reply_to_message.from_user.id, balancremove)
    balances = db.get_balance(message.reply_to_message.from_user.id)
    await message.reply_to_message.reply(f"Баланс пользователя успешно удален на {balancremove} $\nБаланс пользователя: {balances} $ ")
    

@kd.message_handler(commands = ["leaders"], commands_prefix = '!/')
async def cmd_leaders(message: types.Message):
    leaders = db.get_leaderboard()
    await message.reply(f"Лидеры: {leaders}")

@kd.message_handler(commands = ['help'], commands_prefix = '!/')
async def start_command(message: types.Message):
    await message.reply("Помощь по коммандам:\n \nКоманды для модерации:\n\n!mute - Замутить человека на определенное время, используется ответом на сообщение.\n\n!unmute - Снять мут с пользователя, используется ответом на сообщение.\n\n!ban - Забанить пользователя на всегда, используется ответом на сообщение.\n\n!addbalance - Пополнить баланс пользователю, используется ответом на сообщение.\n\n!removebalance - Испольльзуется чтобы понизить баланс пользователю, используется ответом на сообщение.\n\nКоманды для пользователей:\n\n!balance - Узнать свой баланс. ")


@kd.message_handler(commands = ["balance"], commands_prefix = '!/')
async def cmd_balance(message: types.Message):
    balances = db.get_balance(message.from_user.id)
    await message.reply(f"Ваш баланс: {balances} $ ")