import telebot
bot = telebot.TeleBot('5500352575:AAHq_bKD3MVfNSwJCjuH02_IjHnKSBaIqGE')
@bot.message_handler(commands=['start'])
def welcome(message):
    mesg = bot.send_message(message.chat.id,'Please send me message')
    bot.register_next_step_handler(mesg,test)


def test(message):
        msg = bot.send_message(message.chat.id,f'You send me message\n\n{message.text}')
        bot.register_next_step_handler(msg, test1)

def test1(message):
        bot.send_message(message.chat.id, message.text)

bot.infinity_polling(none_stop = True)