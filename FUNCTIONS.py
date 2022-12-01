import telebot, types



def Restart(call):
    InKeyboard = types.InlineKeyboardMarkup(row_width=2)
    but1 = types.InlineKeyboardButton("Узнать ближайшие дедлайны", UserId, callback_data='Know',
                                      message_id=call.message.message_id)
    but2 = types.InlineKeyboardButton("Редактировать", UserId, callback_data='Edit', message_id=call.message.message_id)
    InKeyboard.add(but1)
    if (Admin == True): InKeyboard.add(but2)

    bot.edit_message_text(f"Что вы хотите сделать\nadmin={Admin}\nid={UserId}", UserId,
                          message_id=call.message.message_id, reply_markup=InKeyboard)