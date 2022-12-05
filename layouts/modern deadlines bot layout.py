import telebot
from telebot import types
from dbconfig import Token
import datetime

bot = telebot.TeleBot(Token)

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
year = current_year
month = current_month

ru_month_array = ['Январь', 'Февраль', 'Март', 'Апрель',
               'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
               'Октябрь', 'Ноябрь', 'Декабрь']
callback_for_days = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10',
                     'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19',
                     'd20', 'd21', 'd22', 'd23', 'd24', 'd25', 'd26', 'd27', 'd28',
                     'd29', 'd30', 'd31']
days_array = ['1', '2💀', '3', '4', '5', '6', '7', '8', '9💀', '10', '11', '12', '13',
              '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
              '26', '27', '28', '29', '30', '31']
month_array = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

edit_type = 0

def cancel_markup():
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    keyboard.add(types.InlineKeyboardButton("<<", callback_data = "menu"))
    return keyboard

def calendar_markup(message):
    keyboard = make_calendar_keyboard()
    bot.send_message(message.chat.id, f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}", reply_markup=keyboard)

def make_calendar_keyboard(month = current_month, year = current_year):
    keyboard = types.InlineKeyboardMarkup(row_width= 6)
    quantity_of_days = int

    month = month_array[month-1]
    if month in ['jan','mar','may','jun','aug','oct','dec']:
        quantity_of_days = 31
    elif month == 'feb' and year%400 == 0: quantity_of_days = 29
    elif month == 'feb' and year%100 == 0: quantity_of_days = 28
    elif month == 'feb' and year%4 == 0: quantity_of_days = 29
    elif month == 'feb': quantity_of_days = 28
    else: quantity_of_days = 30

    b1 = types.InlineKeyboardButton('<<год<<', callback_data='previous_year')
    b2 = types.InlineKeyboardButton('>>год>>', callback_data='next_year')
    b3 = types.InlineKeyboardButton('<<месяц<<', callback_data='previous_month')
    b4 = types.InlineKeyboardButton('>>месяц>>', callback_data='next_month')

    keyboard.add(b1, b2)
    keyboard.add(b3, b4)

    current = 0
    DBR = []


    for k in range(quantity_of_days // 6):
        for k in range(6):
            DBR += [types.InlineKeyboardButton(days_array[current], callback_data=callback_for_days[current])]
            current+=1
        keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3], DBR[4], DBR[5])
        DBR = []

    for k in range(quantity_of_days % 6):
        DBR += [types.InlineKeyboardButton(days_array[current], callback_data=callback_for_days[current])]
        current += 1

    if quantity_of_days % 6 == 1: keyboard.add(DBR[0])
    if quantity_of_days % 6 == 4: keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3])
    if quantity_of_days % 6 == 5: keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3], DBR[4])

    keyboard.add(types.InlineKeyboardButton("<<", callback_data="menu"))

    return keyboard

def main():
    @bot.message_handler(commands=['start'])
    def start(message):
        global edit_type
        edit_type = 3
        bot.send_message(message.chat.id, "This is layout of deadlines bot\n\nCommands:\n"
                         "1./admin_menu\n2./user_menu")

    @bot.message_handler(commands=['admin_menu'])
    def admin_menu(message):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = types.KeyboardButton("ближайшие 5 дедлайнов")
        b2 = types.KeyboardButton("календарь")
        b3 = types.KeyboardButton("добавить")
        b4 = types.KeyboardButton("удалить")
        keyboard.add(b1,b2,b3,b4)
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboard)

    @bot.message_handler(commands=['user_menu'])
    def user_menu(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("ближайшие 5 дедлайнов")
        b2 = types.KeyboardButton("календарь")
        keyboard.add(b1, b2)
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboard)

    @bot.message_handler(regexp='добавить')
    def add(message):
        global edit_type
        edit_type = 1
        calendar_markup(message)

    @bot.message_handler(regexp='удалить')
    def delete(message):
        global edit_type
        edit_type = 2
        calendar_markup(message)

    @bot.message_handler(regexp='календарь')
    def calendar(message):
        global edit_type
        edit_type = 0
        calendar_markup(message)

    @bot.callback_query_handler(func = lambda call: True)
    def callbacks(call):
        global year, month
        if call.data in ['previous_year', 'next_year', 'previous_month', 'next_month']:

            if call.data == 'previous_year':
                year -= 1
            if call.data == 'next_year':
                year += 1
            if call.data == 'previous_month':
                month -= 1
                if month == 0:
                    month = 12
            if call.data == 'next_month':
                month += 1
                if month == 13:
                    month = 1

            bot.edit_message_text(f"Год: {year}\nМесяц: {ru_month_array[month - 1]}", chat_id=call.from_user.id, message_id=call.message.message_id)
            keyboard = make_calendar_keyboard(month, year)
            bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)
            return

        if call.data == "menu":
            bot.delete_message(call.from_user.id, message_id = call.message.message_id)
            start(call.message)

        if edit_type == 0:
            bot.edit_message_text("Дедлайны на эту дату:\n\n1. *deadline1*\n2. *deadline2*", chat_id=call.from_user.id, message_id=call.message.message_id)

        if edit_type == 1:
            bot.edit_message_text("Введите, что нужно сдать в этот день", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=cancel_markup())

        if edit_type == 2:
            bot.edit_message_text("Дедлайны на эту дату:\n\n1. *deadline1*\n2. *deadline2*\n\nВведите номер удаляемого дедлайна", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=cancel_markup())

    @bot.message_handler(regexp='ближайшие 5 дедлайнов')
    def nearest_five(message):
        bot.send_message(message.chat.id, '1. *date\n*deadline*\n\n2. *date\n*deadline*\n\n3. *date\n*deadline*\n\n4. *date\n*deadline*\n\n5. *date*:\n*deadline*')

if __name__ == "__main__":
    main()

bot.polling(long_polling_timeout=30)