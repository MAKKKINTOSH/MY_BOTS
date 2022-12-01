import telebot
from functions import DeadDb
from config import Token
from telebot import types

bot=telebot.TeleBot(Token)
DB=DeadDb('deadline_data_base.db')



edit_access = 0
ObjectType = ''
DeadlineDate = ''

def main():

    @bot.message_handler(commands=['start'])
    def Hello(message):

        ReKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)            #<strike>САСУ</strike>
        ReKeyboard.add('Меню')
        bot.send_message(message.chat.id, f'Привет, <b>{message.from_user.first_name}</b>, я - бот твоей любимой группы <b>АСУб-22-1</b>, через меня ты можешь узнать свои ближайшие дедлайны\n\n<u>Важно</u>\n кнопка снизу автоматически возвращает тебя в начало, не бойся ей пользоваться, если вдруг что-то пойдет не так \n\nP.S. <i>Если вдруг что-то не нравится, есть предложение или бот упал и не хочет вставать, все вопросы человеку по ссылке</i>\n\n https://t.me/Van_Vanskiy', reply_markup=ReKeyboard, parse_mode='html')
    @bot.message_handler(regexp='Меню')
    def Menu(message):

        #print(message.chat.id, message.from_user.first_name, message.from_user.last_name)
        #DELETE ON RELEASE

        DB.auto_delete_deadline()

        InKeyboard=types.InlineKeyboardMarkup(row_width=2)
        but1 = types.InlineKeyboardButton("ближайшие дедлайны", callback_data='Know')
        but2 = types.InlineKeyboardButton("Ближайшие 5 дедлайнов", callback_data='Know_five')
        but3 = types.InlineKeyboardButton("✏Добавить✏", callback_data='Edit')
        but4 = types.InlineKeyboardButton("✂Удалить✂", callback_data='Delete')
        InKeyboard.add(but1, but2)
        if (message.chat.id==545762112 or message.chat.id==958029367 or message.chat.id==1960549912 or message.chat.id==1340299205): InKeyboard.add(but3, but4)

        bot.send_message(message.chat.id, f"Что вы хотите сделать", reply_markup=InKeyboard)

        @bot.callback_query_handler(func=lambda call:True)
        def Choise(call):
            print("***", call.data, "***")

            CallData = ['InProf', 'Nosyreva', 'English', 'Informatics', 'Math', 'BBC', 'Prog', 'Physics', 'PE']
            global edit_access, ObjectType, DeadlineDate

            InKeyboard = types.InlineKeyboardMarkup(row_width=2)                                    #object_id
            but1 = types.InlineKeyboardButton('Введение в ПД', callback_data='InProf')                        #1
            but2 = types.InlineKeyboardButton('Дискретная математика', callback_data='Nosyreva')    #2
            but3 = types.InlineKeyboardButton('Иностранный язык', callback_data='English')          #3
            but4 = types.InlineKeyboardButton('Информатика', callback_data='Informatics')           #4
            but5 = types.InlineKeyboardButton('Математика', callback_data='Math')                   #5
            but6 = types.InlineKeyboardButton('ОДК', callback_data='BBC')                           #6
            but7 = types.InlineKeyboardButton('Программирование', callback_data='Prog')             #7
            but8 = types.InlineKeyboardButton('Физика', callback_data='Physics')                    #8
            but9 = types.InlineKeyboardButton('Физкультура', callback_data='PE')                    #9
            but10 = types.InlineKeyboardButton('В меню', callback_data='ToMenu')
            InKeyboard.add(but1, but2, but3, but4, but5, but6, but7, but8, but9, but10)

            InKeyboardType = types.InlineKeyboardMarkup(row_width=3)
            but11 = types.InlineKeyboardButton('Д/З', callback_data='0')
            but12 = types.InlineKeyboardButton('Л/Р', callback_data='1')
            InKeyboardType.add(but11, but12, but10)

            EndKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
            but21 = types.InlineKeyboardButton('В начало', callback_data='ToStart')
            EndKeyboardMarkup.add(but21)

            if call.data=="Know":

                edit_access=0
                bot.edit_message_text('Выберите предмет', call.from_user.id, message_id=call.message.message_id)
                bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id, reply_markup=InKeyboard)

            if call.data=="Know_five":

                bot.edit_message_text(f"Ближайшие 5 дедлайнов\n"
                                      f"1. {DB.show_n_deadline(1)}\n"
                                      f"2. {DB.show_n_deadline(2)}\n"
                                      f"3. {DB.show_n_deadline(3)}\n"
                                      f"4. {DB.show_n_deadline(4)}\n"
                                      f"5. {DB.show_n_deadline(5)}\n", call.from_user.id, message_id=call.message.message_id)
                #bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id, reply_markup=EndKeyboardMarkup )

            if call.data=="Edit":

                edit_access=1
                bot.edit_message_text('Выберите предмет', call.from_user.id, message_id=call.message.message_id)
                bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id, reply_markup=InKeyboard)

            if call.data=="Delete":

                edit_access=2
                bot.edit_message_text('Выберите предмет', call.from_user.id, message_id=call.message.message_id)
                bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id, reply_markup=InKeyboard)

            if call.data == 'ToMenu':

                bot.delete_message(call.from_user.id, message_id=call.message.message_id)
                Menu(call.message)

            if call.data in CallData:
                ObjectType = call.data
                if edit_access == 1:
                    bot.edit_message_text('Д/З или Л/Р', call.from_user.id, message_id=call.message.message_id)
                    bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id, reply_markup=InKeyboardType)
                if edit_access == 0:
                    #print(DB.show_deadline(ObjectType, 0))     #DELETE ON RELEASE
                    #print(DB.show_deadline(ObjectType, 1))     #DELETE ON RELEASE
                    bot.edit_message_text(text=f"Ближайшие дедлайны\n{DB.object(ObjectType)}\nД/З: {DB.show_deadline(ObjectType, 0)}\nЛ/Р: {DB.show_deadline(ObjectType, 1)}", message_id=call.message.message_id, chat_id=call.from_user.id, parse_mode='HTML')
                    #bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id, reply_markup=EndKeyboardMarkup )
                if edit_access == 2:
                    bot.edit_message_text(f"<i>{DB.object(ObjectType)}</i>\nВведите номер дедлайна, который вы хотите удалить\n<b><u>❗❗❗АХТУНГ❗❗❗, отменить удаление нельзя</u></b>\n\n<i>Если передумали удалять, введите что угодно, но не номер дедлайна</i>\n\n{DB.show_all_deadline(ObjectType)}", message_id=call.message.message_id, chat_id=call.from_user.id, parse_mode='html')
                    @bot.message_handler(content_types=['text'])
                    def delete_number(message):
                        n = message.text
                        try:
                            DB.delete_deadline(ObjectType, int(n))
                            bot.send_message(message.chat.id, "✅Отлично, дедлайн успешно удален✅")
                        except: bot.send_message(message.chat.id, "🚫Ошибка, вы неправильно ввели номер🚫")
                        finally:
                            print(edit_access, ObjectType, message.text)
                            Menu(message)

            if call.data == '1' or call.data == '0':
                bot.send_message(call.from_user.id, f'{DB.object(ObjectType)}\n{"Д/З" if call.data == "0" else "Л/Р"}\nВведите дату в формате дд.мм.гггг\n\n<i>Если передумал, введи что-угодно, но не дату</i>', parse_mode='html')
                @bot.message_handler(content_types=['text'])
                def make(message):
                    a = message.text
                    try:
                        DeadlineDate = a[6] + a[7] + a[8] + a[9] + '-' + a[3] + a[4] + '-' + a[0] + a[1]
                        DB.make_deadline(ObjectType, int(call.data), DeadlineDate)
                        bot.send_message(message.chat.id, "✅Отлично, дедлайн успешно внесен✅")
                    except: bot.send_message(message.chat.id, "🚫Ошибка, вы неправильно ввели дату🚫")
                    finally:
                        print(edit_access, call.data, message.text)
                        Menu(message)
                    #bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id, reply_markup=EndKeyboardMarkup )

            #if call.data == "ToStart":
               #Menu(message)


main()

bot.polling(long_polling_timeout=30)            #bot.polling(non_stop=True)

