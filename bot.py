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
from database import *

# токен бота
bot = telebot.TeleBot(token)


#проверка существавания базы данных
check_and_create_db()


#опрос этой недели
@bot.message_handler(commands=['this_week_poll'])
def this_week_poll(message):
    bot.send_poll(message.chat.id, 'Играем?', this_week(), is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)


# опрос след. недели
@bot.message_handler(commands=['next_week_poll'])
def next_week_poll(message):
	bot.send_poll(message.chat.id, 'Играем?', next_week(), is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)


# большой опрос этой. недели
@bot.message_handler(commands=['this_week_poll_ex'])
def this_week_poll_ex(message):
	for i in range(7):
		data = this_day(i)
		bot.send_poll(message.chat.id, data[0], data[1:], is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)


# большой опрос след. недели
@bot.message_handler(commands=['next_week_poll_ex'])
def next_week_poll_ex(message):
	for i in range(7, 14):
		data = this_day(i)
		bot.send_poll(message.chat.id, data[0], data[1:], is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)


#прикрепление ссылки на рейтинг
@bot.message_handler(commands=['add_rating_link'])
def add_rating_link(message):
	#ищем первое числовое значение в строке рейтинга (оно единственное) и записываем в переменную
	try:
		pantheon_id = [int(part) for part in message.text.split('/') if part.isdigit()][0]
		check_chat = fetch_one(f"SELECT chat_id FROM chats WHERE chat_id = {message.chat.id}")
	        
		if not check_chat:
	    # Добавляем чат, если его нет
			simple_execute(f"INSERT INTO chats (chat_id, chat_only_mod) VALUES ({message.chat.id}, 0)")
			bot.send_message(message.chat.id, 'Ссылка добавлена', message_thread_id= message.message_thread_id)
		pantheon_name = get_rating_name(pantheon_id)
		simple_execute(f"INSERT INTO links (chat_id, pantheon_id, pantheon_name, pantheon_sorting, pantheon_filter) VALUES ({message.chat.id}, {pantheon_id}, '{pantheon_name}', 'rating', NULL)")
		bot.send_message(message.chat.id, 'Ссылка добавлена', message_thread_id= message.message_thread_id)
	except:
		bot.send_message(message.chat.id, 'добавить рейтинг не удалось!', message_thread_id= message.message_thread_id)


#вывод списка команд
@bot.message_handler(commands=['help', 'commands'])
def help(message):
	bot.send_message(message.chat.id, help_info, message_thread_id= message.message_thread_id)
#запуск бота
bot.polling(none_stop = True)