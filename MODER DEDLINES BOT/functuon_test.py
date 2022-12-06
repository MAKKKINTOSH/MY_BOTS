import time
import sqlite3
from DBfunctions import data_base
import datetime
a = data_base('data_base.db')
#my_id = 545762112

#a.make_deadline("evmb-22-2", 10, 3, 2022, "asdas")
#a.delete_deadline("evmb-22-2", 30, 1, 2022, 1)
#print(a.show_deadline("evmb-22-2", 10, 3, 2022))

#a = []
#
#for k in range(5):
#    a += [{'id' : k, 'num' : k*2}]
#
#for k in range(len(a)):
#    if a[k]['id'] == 4:
#        print(k)


#b = []
#for k in range(30000):
#    b+=[{'id' : k*2, 'group' : f"asu-22-{k}", 'date' : k}]
#
#start = time.time()
#
#for k in range(len(b)):
#    if b[k]['id'] == -1:
#        print("a")
#
#end = time.time()
#
#print(end - start)
#
#


#start = time.time()
#
#print(a.show_deadline("asub-22-1", 30, 1, 2000))
#
#
#end = time.time()
#
#print(end - start)

#start = time.time()
#print(start)
#
#day = datetime.datetime.now().day
#month = datetime.datetime.now().month
#year = datetime.datetime.now().year
#
#end = time.time()
#print(end)
#
#print(end - start)

@bot.message_handler(commands=['start'])
def welcome(message):
    mesg = bot.send_message(message.chat.id,'Please send me message')
    bot.register_next_step_handler(mesg,test)


def test(message):
    bot.send_message(message.chat.id,'You send me message')