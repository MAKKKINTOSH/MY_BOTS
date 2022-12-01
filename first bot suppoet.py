import telebot
from telebot import types
token='5500352575:AAHq_bKD3MVfNSwJCjuH02_IjHnKSBaIqGE'
bot=telebot.TeleBot(token)

def er(message):
    bot.send_message(message.chat.id, "Встроенной клавиатурой пользуйся, дебил!")

basedKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
but1=types.KeyboardButton("Да")
basedKeyboard.add(but1)

@bot.message_handler(commands=['start'])
def kuz(message):

    bot.send_sticker(message.chat.id,open('E:/stickers/welcome_1.webp', 'rb'))
    bot.send_message(message.chat.id, "Welcome to the club, buddy!")
    bot.send_sticker(message.chat.id,open('E:/stickers/welcome_2.webp', 'rb'))
    bot.send_message(message.chat.id, "Хочешь узнать неоспоримую истину этого мира?", reply_markup=basedKeyboard)

@bot.message_handler(content_types=['text'])

def slaves(message):
    if( message.text == 'Да'):
        bot.send_message(message.chat.id, "Кузьмина  сука ебаная")
        bot.send_message(message.chat.id, "Еще?", reply_markup=basedKeyboard)
    else:
        er(message)

bot.polling(none_stop=True)