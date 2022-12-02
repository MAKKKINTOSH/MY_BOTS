import telebot
from telebot import types
from config import Token
import datetime

bot = telebot.TeleBot(Token)

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
year = current_year

ru_month_array = ['Январь', 'Февраль', 'Март', 'Апрель',
               'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
               'Октябрь', 'Ноябрь', 'Декабрь']

def make_calendar_keyboard(month = current_month, year = current_year):
    keyboard = types.InlineKeyboardMarkup(row_width= 6)
    quantity_of_days = int
    callback_for_days = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10',
                             'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19',
                             'd20', 'd21', 'd22', 'd23', 'd24', 'd25', 'd26', 'd27', 'd28',
                             'd29', 'd30', 'd31']
    days_array = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                         '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
                         '26', '27', '28', '29', '30', '31']
    month_array = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    edit_access = 0
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

    return keyboard

def main():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "<b>МЕНЮ</b>\n\nКоманды: /calendar", parse_mode='html')

    @bot.message_handler(commands=['calendar'])
    def calendar(message, year = current_year, month = current_month):
        keyboard = make_calendar_keyboard()
        bot.send_message(message.chat.id, f"Год: {year}\nМесяц: {ru_month_array[month - 1]}", parse_mode='html', reply_markup=keyboard)
        bot.register_next_step_handler_by_chat_id(message.chat.id, edit)


    @bot.callback_query_handler(func = lambda call:True)
    def edit(call):
        if call.data == 'previous_year':
            calendar(call.message, current_year - 1, current_month)



if __name__ == "__main__":
    main()

bot.polling(long_polling_timeout=30)