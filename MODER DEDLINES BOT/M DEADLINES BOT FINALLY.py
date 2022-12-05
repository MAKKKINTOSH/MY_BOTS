import telebot
from telebot import types
from DBfunctions import data_base
from config import Token
from datetime import datetime

bot = telebot.TeleBot(Token)
DB = data_base('data_base.db')

current_year = datetime.now().year
current_month = datetime.now().month
current_day = datetime.now().day

days_array = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
              '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
              '26', '27', '28', '29', '30', '31']
callback_for_days = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08', 'd09', 'd10',
                     'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19',
                     'd20', 'd21', 'd22', 'd23', 'd24', 'd25', 'd26', 'd27', 'd28',
                     'd29', 'd30', 'd31']

month_array = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
ru_month_array = ['Январь', 'Февраль', 'Март', 'Апрель',
               'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
               'Октябрь', 'Ноябрь', 'Декабрь']

groups_array = ["АСУб-22-1", "ЭВМб-22-2"]
callback_for_groups = ["asub-22-1", "evmb-22-2"]
groups_size = len(groups_array)

admins = [{'id' : 545762112, 'group' : "asub-22-1"}]
admins_size = len(admins)

users = []

def is_admin(id, group):
    for k in range(admins_size):
        if id == admins[k]['id']:
            if group == admins[k]['group']:
                return True
            return False

def take_group(id):
    for k in users:
        if k['id'] == id:
            return k['group']

def make_cancel_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    keyboard.add(types.InlineKeyboardButton("<<", callback_data = "menu"))
    return keyboard

def make_registration_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for k in range(groups_size):
        keyboard.add(types.InlineKeyboardButton(groups_array[k], callback_data=callback_for_groups[k]))
    return keyboard

def make_menu_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = types.KeyboardButton("ближайшие 5 дедлайнов")
    b2 = types.KeyboardButton("календарь")
    keyboard.add(b1, b2)

    if is_admin(message.chat.id, take_group(message.chat.id)):
        b3 = types.KeyboardButton("добавить")
        b4 = types.KeyboardButton("удалить")
        keyboard.add(b3, b4)
    return keyboard

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

    @bot.message_handler(commands = ["start"])
    def start(message):
        bot.send_message(message.chat.id, "Привет, я - прототип дедлайн бота, мои команды:\n\n"
                                          "1./reg - выбор вашей группы)\n"
                                          "2./menu - главное меню\n"
                                          "3./help - помощь\n"
                                          "4./contacts - контакты")

        bot.send_message(message.chat.id, "Выберите группу", reply_markup = make_registration_keyboard())

    @bot.message_handler(commands = ["reg"])        #COMPLETE
    def registration(message):
        bot.send_message(message.chat.id, "Выберите группу", reply_markup = make_registration_keyboard())


    @bot.message_handler(commands = ["menu"])       #COMPLETE
    def menu(message):
        bot.send_message(message.chat.id, "Выберите действие", reply_markup = make_menu_keyboard(message))

    @bot.message_handler(commands = ["help"])
    def help(message): ""

    @bot.message_handler(commands = ['contacts'])   #COMPLETE
    def contacts(message):
        bot.send_message(message.chat.id, "Создатели:\n\n"
                                          "Иван - @Van_Vanskiy\n"
                                          "Александр - @chipul1a")

    @bot.message_handler(regexp = 'ближайшие 5 дедлайнов')

    @bot.message_handler(regexp = 'календарь')
    def calendar(message):
        #DB.change_variable(message.chat.id, "edit_type", 0)

        #DB.change_variable(message.chat.id, "selected_year", current_year)
        #DB.change_variable(message.chat.id, "selected_month", current_month)

        bot.send_message(message.chat.id,
                         f"Выберите дату, на которую хотите посмотреть дедлайн\n\n"
                         f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                         reply_markup = make_calendar_keyboard())


    @bot.message_handler(regexp = 'добавить')

    @bot.message_handler(regexp = 'удалить')

    @bot.callback_query_handler(func = lambda call:True)
    def callbacks(call):

        if call.data in callback_for_groups:
            global users
            print(call.from_user.id, call.data)
            for k in range(len(users)):
                if users[k]['id'] == call.from_user.id:
                    users.pop(k)
                    break
            users += [{'id' : call.from_user.id, 'group' : call.data, 'data' : f"{current_year}-{current_month}-{current_day}"}]
            bot.edit_message_text("Вы успешно выбрали группу", chat_id = call.from_user.id, message_id = call.message.message_id)
            return

        if call.data == "menu":
            bot.delete_message(call.from_user.id, message_id=call.message.message_id)
            bot.send_message(call.from_user.id, "Выберите действие")
            return

        if call.data in ['previous_year', 'next_year', 'previous_month', 'next_month']:
            if call.data == 'previous_year':
                #DB.change_date_variable(call.from_user.id, "selected_year", "-")

            if call.data == 'next_year':
                #DB.change_date_variable(call.from_user.id, "selected_year", "+")

            if call.data == 'previous_month':
                #DB.change_date_variable(call.from_user.id, "selected_month", "-")
                if #DB.take_variable(call.from_user.id, "selected_month") == 0:
                    #DB.change_variable(call.from_user.id, "selected_month", 12)

            if call.data == 'next_month':
                #DB.change_date_variable(call.from_user.id, "selected_month", "+")
                if #DB.take_variable(call.from_user.id, "selected_month") == 13:
                    #DB.change_variable(call.from_user.id, "selected_month", 1)


            bot.edit_message_text(f"Год: {#DB.take_variable(call.from_user.id, 'selected_year')}\n"
                                  f"Месяц: {#ru_month_array[DB.take_variable(call.from_user.id, 'selected_month') - 1]}",
                                  chat_id=call.from_user.id,
                                  message_id=call.message.message_id)

            keyboard = make_calendar_keyboard(#DB.take_variable(call.from_user.id, 'selected_month'),
                                              #DB.take_variable(call.from_user.id, 'selected_year'))

            bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                          reply_markup=keyboard)
            return

        if call.data in callback_for_days:
            if #DB.take_variable(call.from_user.id, "edit_type") == 0:
                #DB.show_deadline()

            if #DB.take_variable(call.from_user.id, "edit_type") == 1: ""

            if #DB.take_variable(call.from_user.id, "edit_type") == 2: ""

if __name__ == "__main__":
    main()

bot.polling(long_polling_timeout=5)