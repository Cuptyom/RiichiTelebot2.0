import telebot
from telebot import types
import sqlite3
from days import *
from rating import *
from panteonStats import *
from rating_name import *
from tempai import *
import time
from API import token
from help import help_info

# токен бота
bot = telebot.TeleBot(token)


#опрос этой недели
@bot.message_handler(commands=['this_week_poll'])
def this_week_poll(message):
    bot.send_poll(message.chat.id, 'Играем?', this_week(), is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)


# опрос след. недели
@bot.message_handler(commands=['next_week_poll'])
def this_week_poll(message):
	bot.send_poll(message.chat.id, 'Играем?', next_week(), is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)


#вывод списка команд
@bot.message_handler(commands=['help', 'commands'])
def help(message):
	bot.send_message(message.chat.id, help_info, message_thread_id= message.message_thread_id)
#запуск бота
bot.polling(none_stop = True)