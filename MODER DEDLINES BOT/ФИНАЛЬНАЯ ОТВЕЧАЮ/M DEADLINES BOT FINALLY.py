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

month_array = ['01', '02', '03', '04', '05', '06',
               '07', '08', '09', '10', '11', '12']
ru_month_array = ['Январь', 'Февраль', 'Март', 'Апрель',
               'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
               'Октябрь', 'Ноябрь', 'Декабрь']

groups_array = ["АСУб-22-1", "ЭВМб-22-2"]
callback_for_groups = ["asub-22-1", "evmb-22-2"]
groups_size = len(groups_array)

main_admin = 545762112

admins = DB.take_dictionary('admins', current_month, current_year)
admins_size = len(admins)

users = DB.take_dictionary('users', current_month, current_year)

def is_admin(id, group):
    for k in range(admins_size):
        if id == admins[k]['id']:
            if group == admins[k]['group']:
                return True
            return False

def is_user(id):
    for k in users:
        if k['id'] == id:
            return True
    return False

def take_variable(id, variable):
    for k in users:
        if k['id'] == id:
            return k[variable]

def change_variable(id, variable, value):
    for k in users:
        if k['id'] == id:
            k[variable] = value

def change_date_variable(id, variable, operator):
    for k in users:
        if k['id'] == id:
            var = k[variable]
            if var == 12 and variable == 'month' and operator == '+':
                var = 0
            elif var == 1 and variable == 'month' and operator == '-':
                var = 13
            k[variable] = var - 1 if operator == "-" else var + 1

def show_ru_group_name(group):
    for k in range(len(callback_for_groups)):
        if group == callback_for_groups[k]:
            return groups_array[k]

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

    if is_admin(message.chat.id, take_variable(message.chat.id, 'group')):
        b3 = types.KeyboardButton("добавить")
        b4 = types.KeyboardButton("удалить")
        keyboard.add(b3, b4)

    if message.chat.id == main_admin:
        keyboard.add(types.KeyboardButton("внести админа"))

    return keyboard


def make_calendar_keyboard(group, month = current_month, year = current_year):
    keyboard = types.InlineKeyboardMarkup(row_width= 6)
    quantity_of_days = int

    if month in [1, 3, 5, 6, 8, 10 , 12]:
        quantity_of_days = 31
    elif month == 2 and year % 400 == 0: quantity_of_days = 29
    elif month == 2 and year % 100 == 0: quantity_of_days = 28
    elif month == 2 and year % 4 == 0: quantity_of_days = 29
    elif month == 2: quantity_of_days = 28
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
            text = 'ㅤ' + days_array[current]
            if DB.record_exist(group, days_array[current], month_array[month - 1], year):
                text += '☠'
            else:
                text+='ㅤ'

            DBR += [types.InlineKeyboardButton(text, callback_data=callback_for_days[current])]
            current+=1
        keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3], DBR[4], DBR[5])
        DBR = []

    for k in range(quantity_of_days % 6):
        text = 'ㅤ' + days_array[current]
        if DB.record_exist(group, days_array[current], month_array[month - 1], year):
            text += '☠'
        else:
            text+='ㅤ'

        DBR += [types.InlineKeyboardButton(text, callback_data=callback_for_days[current])]
        current += 1

    if quantity_of_days % 6 == 1: keyboard.add(DBR[0])
    if quantity_of_days % 6 == 4: keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3])
    if quantity_of_days % 6 == 5: keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3], DBR[4])

    keyboard.add(types.InlineKeyboardButton("<<", callback_data="menu"))

    return keyboard

def main():

    @bot.message_handler(commands = ["start"])
    def start(message):
        bot.send_message(message.chat.id, "Привет, я - прототип дедлайн бота\n\n"
                                          "Чтобы узнать команды, используйте /help\n\n"
                                          "Но для начала выберите группу")

        bot.send_message(message.chat.id, "Выберите группу", reply_markup = make_registration_keyboard())

    @bot.message_handler(commands = ["reg"])        #COMPLETE
    def registration(message):
        bot.send_message(message.chat.id, "Выберите группу", reply_markup = make_registration_keyboard())


    @bot.message_handler(commands = ["menu"])       #COMPLETE
    def menu(message):
        if not is_user(message.chat.id):
            bot.send_message(message.chat.id, "Вы не выбрали группу\n\nВыбрать группу можно по команде /reg")
            return
        bot.send_message(message.chat.id, "Выберите действие", reply_markup = make_menu_keyboard(message))

    @bot.message_handler(commands = ["help"])
    def help(message):
        bot.send_message(message.chat.id, "Привет, я - прототип дедлайн бота\n\n"
                                          "1./reg - выбор вашей группы)\n"
                                          "2./menu - главное меню\n"
                                          "3./help - помощь\n"
                                          "4./contacts - контакты")

    @bot.message_handler(commands = ['contacts'])   #COMPLETE
    def contacts(message):
        bot.send_message(message.chat.id, "Создатели:\n\n"
                                          "Иван - @Van_Vanskiy\n"
                                          "Александр - @chipul1a")

    @bot.message_handler(regexp = 'ближайшие 5 дедлайнов')
    def next_five(message):

        if not is_user(message.chat.id):
            bot.send_message(message.chat.id, "Вы не выбрали группу\n\nВыбрать группу можно по команде /reg")
            return

        bot.send_message(message.chat.id, DB.show_next_n_deadline(take_variable(message.chat.id, 'group'), 5))


    @bot.message_handler(regexp = 'календарь')
    def calendar(message):

        if not is_user(message.chat.id):
            bot.send_message(message.chat.id, "Вы не выбрали группу\n\nВыбрать группу можно по команде /reg")
            return

        global current_month, current_year, current_day

        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        change_variable(message.chat.id, "edit_type", 0)
        change_variable(message.chat.id, "year", current_year)
        change_variable(message.chat.id, "month", current_month)

        bot.send_message(message.chat.id,
                         f"Выберите дату, на которую хотите посмотреть дедлайн\n\n"
                         f"Группа: {show_ru_group_name(take_variable(message.chat.id, 'group'))}\n"
                         f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                         reply_markup = make_calendar_keyboard(take_variable(message.chat.id, 'group')))

    @bot.message_handler(regexp = 'добавить')
    def add(message):
        if not is_user(message.chat.id):
            bot.send_message(message.chat.id, "Вы не выбрали группу\n\nВыбрать группу можно по команде /reg")
            return

        if not is_admin(message.chat.id, take_variable(message.chat.id, 'group')):
            bot.send_message(message.chat.id, "Вы не являетесь админом этой группы")
            return

        change_variable(message.chat.id, 'edit_type', 1)
        change_variable(message.chat.id, "year", current_year)
        change_variable(message.chat.id, "month", current_month)

        bot.send_message(message.chat.id,
                         f"Выберите дату, на которую хотите добавить дедлайн дедлайн\n\n"
                         f"Группа: {show_ru_group_name(take_variable(message.chat.id, 'group'))}\n"
                         f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                         reply_markup=make_calendar_keyboard(take_variable(message.chat.id, 'group')))

    @bot.message_handler(regexp = 'удалить')
    def delete(message):
        if not is_user(message.chat.id):
            bot.send_message(message.chat.id, "Вы не выбрали группу\n\nВыбрать группу можно по команде /reg")
            return

        if not is_admin(message.chat.id, take_variable(message.chat.id, 'group')):
            bot.send_message(message.chat.id, "Вы не являетесь админом этой группы")
            return

        change_variable(message.chat.id, 'edit_type', 2)
        change_variable(message.chat.id, "year", current_year)
        change_variable(message.chat.id, "month", current_month)

        bot.send_message(message.chat.id,
                         f"Выберите дату, на которую вы хотите удалить дедлайн\n\n"
                         f"Группа: {show_ru_group_name(take_variable(message.chat.id, 'group'))}\n"
                         f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                         reply_markup=make_calendar_keyboard(take_variable(message.chat.id, 'group')))

    @bot.message_handler(regexp = "внести админа")
    def add_admin(message):
        if message.chat.id != main_admin:
            bot.send_message(message.chat.id, "Это не для тебя")
            return

        mesg = bot.send_message(message.chat.id, 'Введите id', reply_markup=make_cancel_keyboard())
        bot.register_next_step_handler(mesg, take_id)

    def take_id(message):
        id = message.text
        mesg = bot.send_message(message.chat.id, 'Введите группу', reply_markup=make_cancel_keyboard())
        bot.register_next_step_handler(mesg, take_group, id)

    def take_group(message, id):
        global admins
        for k in range(len(groups_array)):

            if groups_array[k] == message.text:

                group = callback_for_groups[k]
                DB.make_admin(id, group)

                for m in range(len(admins)):
                    if admins[m]['id'] == int(id):
                        admins.pop(m)
                        break

                admins+=[{'id' : int(id),
                          'group' : group}]

                bot.send_message(message.chat.id, "Админ добавлен")
                return
        bot.send_message(message.chat.id, "вы неправильно указали группу")
        return

    @bot.callback_query_handler(func = lambda call:True)
    def callbacks(call):

        if call.data in callback_for_groups:
            global users
            print(call.from_user.id, call.data)
            for k in range(len(users)):
                if users[k]['id'] == call.from_user.id:
                    users.pop(k)
                    break

            users += [{'id' : call.from_user.id,
                       'group' : call.data,
                       'month' : current_month,
                       'year' : current_year,
                       'edit_type' : 3}]
            DB.make_user(call.from_user.id, call.data)

            bot.edit_message_text("Вы успешно выбрали группу", chat_id = call.from_user.id, message_id = call.message.message_id)

        if call.data == "menu":
            bot.clear_step_handler_by_chat_id(chat_id=call.from_user.id)
            bot.delete_message(call.from_user.id, message_id=call.message.message_id)
            bot.send_message(call.from_user.id, "Выберите действие")


        if call.data in ['previous_year', 'next_year', 'previous_month', 'next_month']:
            if call.data == 'previous_year':
                    change_date_variable(call.from_user.id, "year", '-')

            if call.data == 'next_year':
                change_date_variable(call.from_user.id, "year", '+')

            if call.data == 'previous_month':
                change_date_variable(call.from_user.id, "month", '-')

            if call.data == 'next_month':
                change_date_variable(call.from_user.id, "month", '+')

            set_year = take_variable(call.from_user.id, 'year')
            set_month = take_variable(call.from_user.id, 'month')

            type = take_variable(call.from_user.id, 'edit_type')
            if type == 0:
                text = "ВЫберите дату, на которую хотите посмотреть дедлайн"
            elif type == 1:
                text = "Выберите дату, на которую хотите добавить дедлайн дедлайн"
            else:
                text = "Выберите дату, на которую вы хотите удалить дедлайн"


            bot.edit_message_text(f"{text}\n\n"
                                  f"Группа: {show_ru_group_name(take_variable(call.from_user.id, 'group'))}\n"
                                  f"Год: {set_year}\n"
                                  f"Месяц: {ru_month_array[set_month - 1]}",
                                  chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=make_calendar_keyboard(take_variable(call.from_user.id, 'group'), set_month, set_year))


        if call.data in callback_for_days:
            if take_variable(call.from_user.id, 'edit_type') == 0:

                set_group = take_variable(call.from_user.id, 'group')
                set_day = call.data[1:]
                set_month = month_array[take_variable(call.from_user.id, 'month') - 1]
                set_year = take_variable(call.from_user.id, 'year')

                bot.edit_message_text(DB.show_deadline(set_group, set_day, set_month, set_year),
                                      chat_id = call.from_user.id,
                                      message_id = call.message.message_id)

            if take_variable(call.from_user.id, 'edit_type') == 1:

                set_day = call.data[1:]
                set_month = month_array[take_variable(call.from_user.id, 'month') - 1]
                set_year = take_variable(call.from_user.id, 'year')

                mesg = bot.edit_message_text(f"Введите дедлайн на {set_day}.{set_month}.{set_year}", call.from_user.id, call.message.message_id, reply_markup = make_cancel_keyboard())
                bot.register_next_step_handler(mesg, add_deadline, call.data[1:])


            if take_variable(call.from_user.id, 'edit_type') == 2:

                mesg = bot.edit_message_text(f"{DB.show_deadline(take_variable(call.from_user.id, 'group'), call.data[1:], month_array[take_variable(call.from_user.id, 'month') - 1], take_variable(call.from_user.id, 'year'))}\n\nВведите номер дедлайна, который хотите удалить", call.from_user.id, call.message.message_id, reply_markup=make_cancel_keyboard())

                bot.register_next_step_handler(mesg, delete_deadline, call.data[1:])
    def add_deadline(message, day):

        DB.make_deadline(take_variable(message.chat.id, "group"),
                         day,
                         month_array[take_variable(message.chat.id, 'month') - 1],
                         take_variable(message.chat.id, "year"),
                         message.text)

        bot.send_message(message.chat.id, "Дедлайн внесен")

    def delete_deadline(message, day):
        try:
            DB.delete_deadline(take_variable(message.chat.id, "group"),
                               day,
                               month_array[take_variable(message.chat.id, 'month') - 1],
                               take_variable(message.chat.id, "year"),
                               int(message.text))

            bot.send_message(message.chat.id, "✅Отлично, дедлайн успешно удален✅")

        except: bot.send_message(message.chat.id, "🚫Ошибка, вы неправильно ввели номер🚫")
        finally:
            pass




if __name__ == "__main__":
    main()

bot.polling(long_polling_timeout=5, none_stop=True)