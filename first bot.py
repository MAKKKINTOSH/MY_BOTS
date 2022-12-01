import telebot
import sqlite3
import datetime
from config import Token
from telebot import types

bot=telebot.TeleBot(Token)
DB=sqlite3.connect('deadlines bot/deadline_data_base.db')

Admin=bool
UserId=int
edit_access = 0

def  deadlines(object): ''


def main():

    @bot.message_handler(commands=['start'])
    def Hello(message):
        global UserId
        UserId = message.chat.id
        ReKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        ReKeyboard.add('Запуск')
        bot.send_message(UserId, f'Привет, {UserId},через меня ты можешь узнать свои ближайшие дедлайны', reply_markup=ReKeyboard)
    @bot.message_handler(regexp='Запуск')
    def Menu(message):


        Admin=False
        if UserId==545762112 or UserId==958029367:
            Admin=True

        InKeyboard=types.InlineKeyboardMarkup(row_width=3)
        but1 = types.InlineKeyboardButton("ближайшие дедлайны", callback_data='Know')
        but2 = types.InlineKeyboardButton("Ближайшие 5 дедлайнов", callback_data='Know_five')
        but3 = types.InlineKeyboardButton("Редактировать", callback_data='Edit')
        InKeyboard.add(but1, but2)
        if (Admin==True): InKeyboard.add(but3)

        bot.send_message(UserId, f"Что вы хотите сделать\nadmin={Admin}\nid={UserId}", reply_markup=InKeyboard)

        @bot.callback_query_handler(func=lambda call:True)
        def Choise(call):

            global edit_access

            InKeyboard = types.InlineKeyboardMarkup(row_width=2)                                    #object_id
            but1 = types.InlineKeyboardButton('ВПД', callback_data='InProf')                  #1
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

            InKeyboardType = types.InlineKeyboardButton


            if call.data=="Know":

                bot.edit_message_text('Выберите предмет', UserId, message_id=call.message.message_id)
                bot.edit_message_reply_markup(UserId, message_id=call.message.message_id, reply_markup=InKeyboard)

            if call.data=="Know_five":

                bot.answer_callback_query(call.id, text="еще не готово", show_alert=True)

            if call.data=="Edit":

                edit_access=1
                bot.edit_message_text('Выберите предмет', UserId, message_id=call.message.message_id)
                bot.edit_message_reply_markup(UserId, message_id=call.message.message_id, reply_markup=InKeyboard)

            if call.data == 'InProf' and edit_access==1: " "

            if call.data == 'Nosyreva' and edit_access==1: " "

            if call.data == 'English' and edit_access==1: " "
" "
            if call.data == 'Informatics' and edit_access==1: " "

            if call.data == 'Math' and edit_access==1: " "

            if call.data == 'BBC' and edit_access==1: " "

            if call.data == 'Prog' and edit_access==1: " "

            if call.data == 'Physics' and edit_access==1: " "

            if call.data == 'PE' and edit_access==1: " "

            if call.data == 'InProf' and edit_access==0: " "

            if call.data == 'Nosyreva' and edit_access==0: " "

            if call.data == 'English' and edit_access==0: " "

            if call.data == 'Informatics' and edit_access==0: " "

            if call.data == 'Math' and edit_access==0: " "

            if call.data == 'BBC' and edit_access==0: " "

            if call.data == 'Prog' and edit_access==0: " "

            if call.data == 'Physics' and edit_access==0: " "

            if call.data == 'PE' and edit_access==0: " "

            if call.data == 'ToMenu':

                bot.delete_message(UserId, message_id=call.message.message_id)
                Menu(call.message)



main()

bot.polling(long_polling_timeout=30)            #bot.polling(non_stop=True)