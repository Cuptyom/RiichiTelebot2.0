import telebot
from telebot import types
import sqlite3
from days import *
from rating import *
from panteonStats import *
from rating_name import *
import time
from API import token
from help import help_info
from database import *
import schedule
import threading
from achievements import *

# токен бота
bot = telebot.TeleBot(token)

#ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

#проверка существавания базы данных
check_and_create_db()

def add_this_chat_if_not_exist(chat_id):
	check_chat = fetch_one("SELECT chat_id FROM chats WHERE chat_id = ?", (chat_id,))        
	if not check_chat:
    # Добавляем чат, если его нет
		simple_execute("INSERT INTO chats (chat_id) VALUES (?)", (chat_id,))

#функция, проверяющая времяд для опросов
def send_weekly_polls_in_chats():
	try:
		chats = fetch_all("SELECT chat_id, topic_id, poll_type FROM weekly_poll")
		for chat in chats:
			time.sleep(1) #чтобы не нагружать слабую машину
			if chat[2] == 'normal':
				bot.send_poll(chat[0], 'Играем?', this_week(), is_anonymous = False, allows_multiple_answers = True, message_thread_id= chat[1])
			else:
				for i in range(7):
					data = this_day(i)
					bot.send_poll(chat[0], data[0], data[1:], is_anonymous = False, allows_multiple_answers = True, message_thread_id= chat[1])
	except:
		pass
#шедулер для проверки времени
def scheduler():
    """Запускает планировщик в отдельном потоке."""
    schedule.every().monday.at("00:01").do(send_weekly_polls_in_chats)
    # Для отладки можно раскомментировать:
    #schedule.every(1).minutes.do(send_weekly_polls_in_chats)
    while True:
        schedule.run_pending()
        time.sleep(10)
# Запуск планировщика в демоническом потоке (завершится при завершении главного)
scheduler_thread = threading.Thread(target=scheduler, daemon=True)
scheduler_thread.start()


#ОСНОВНЫЕ ФУНКЦИИ БОТА
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
		add_this_chat_if_not_exist(message.chat.id)
		pantheon_id = [int(part) for part in message.text.split('/') if part.isdigit()][0]
		pantheon_name = get_rating_name(pantheon_id)
		simple_execute("INSERT INTO links (chat_id, pantheon_id, pantheon_name, pantheon_sorting, pantheon_filter) VALUES (?, ?, ?, 'rating', NULL)", (message.chat.id, pantheon_id, pantheon_name))
		bot.send_message(message.chat.id, 'Ссылка добавлена', message_thread_id= message.message_thread_id)
	except:
		bot.send_message(message.chat.id, 'добавить рейтинг не удалось!', message_thread_id= message.message_thread_id)


#вывод рейтинговой таблицы
@bot.message_handler(commands=['show_rating_table'])
def show_rating_table(message):
	#try:
		add_this_chat_if_not_exist(message.chat.id)
		ratings_list = fetch_all("SELECT pantheon_name, pantheon_id, pantheon_sorting, pantheon_filter FROM links WHERE chat_id = ?", (message.chat.id,))
		if not ratings_list:
			bot.send_message(message.chat.id, 'Вы еще не прикрепляли рейтинг!', message_thread_id= message.message_thread_id)
			return 0
		markup = types.InlineKeyboardMarkup()
		for rating in ratings_list:
			markup.add(types.InlineKeyboardButton(text=f"{rating[0]}", callback_data=f'show_rating_table|{rating[1]}|{rating[2]}|{rating[3]}'))
		bot.send_message(message.chat.id,"Выбор рейтинга", reply_markup=markup, message_thread_id=message.message_thread_id)
	#except:
		#bot.send_message(message.chat.id, 'вывести список прикрепленных рейтингов не удалось!', message_thread_id= message.message_thread_id)

#удалить ссылку на рейтинг.
@bot.message_handler(commands=['delete_rating_link'])
def delete_rating_link(message):
	try:
		add_this_chat_if_not_exist(message.chat.id)
		ratings_list = fetch_all("SELECT pantheon_name, pantheon_id FROM links WHERE chat_id = ?", (message.chat.id,))
		if not ratings_list:
			bot.send_message(message.chat.id, 'Вы еще не прикрепляли рейтинг!', message_thread_id= message.message_thread_id)
			return 0
		markup = types.InlineKeyboardMarkup()
		for rating in ratings_list:
			markup.add(types.InlineKeyboardButton(text=f"{rating[0]}", callback_data=f'delete_rating_table|{message.chat.id}|{rating[1]}'))
		bot.send_message(message.chat.id,"Выбор рейтинга", reply_markup=markup, message_thread_id=message.message_thread_id)
	except:
		bot.send_message(message.chat.id, 'вывести список прикрепленных рейтингов не удалось!', message_thread_id= message.message_thread_id)


#настройки парсинга рейтинга
@bot.message_handler(commands=['rating_table_settings'])
def rating_table_settings(message):
	try:
		add_this_chat_if_not_exist(message.chat.id)
		ratings_list = fetch_all("SELECT pantheon_name, pantheon_id FROM links WHERE chat_id = ?", (message.chat.id,))
		if not ratings_list:
			bot.send_message(message.chat.id, 'Вы еще не прикрепляли рейтинг!', message_thread_id= message.message_thread_id)
			return 0
		markup = types.InlineKeyboardMarkup()
		for rating in ratings_list:
			markup.add(types.InlineKeyboardButton(text=f"{rating[0]}", callback_data=f'rating_table_settings|{message.chat.id}|{rating[1]}'))
		bot.send_message(message.chat.id,"Выбор рейтинга", reply_markup=markup, message_thread_id=message.message_thread_id)
	except:
		bot.send_message(message.chat.id, 'вывести список прикрепленных рейтингов не удалось!', message_thread_id= message.message_thread_id)

# парсинг статистики по яку
@bot.message_handler(commands=['yaku_stats'])
def yaku_stats(message):
	try:
		add_this_chat_if_not_exist(message.chat.id)
		ratings_list = fetch_all("SELECT pantheon_name, pantheon_id FROM links WHERE chat_id = ?", (message.chat.id,))
		if not ratings_list:
			bot.send_message(message.chat.id, 'Вы еще не прикрепляли рейтинг!', message_thread_id= message.message_thread_id)
			return 0
		markup = types.InlineKeyboardMarkup()
		for rating in ratings_list:
			markup.add(types.InlineKeyboardButton(text=f"{rating[0]}", callback_data=f'yaku_stats|{rating[1]}'))
		bot.send_message(message.chat.id,"Выбор рейтинга", reply_markup=markup, message_thread_id=message.message_thread_id)
	except:
		bot.send_message(message.chat.id, 'вывести список прикрепленных рейтингов не удалось!', message_thread_id= message.message_thread_id)


#статистика по ачивкам
@bot.message_handler(commands=['achievements_stats'])
def achievements_stats(message):
	try:
		add_this_chat_if_not_exist(message.chat.id)
		ratings_list = fetch_all("SELECT pantheon_name, pantheon_id FROM links WHERE chat_id = ?", (message.chat.id,))
		if not ratings_list:
			bot.send_message(message.chat.id, 'Вы еще не прикрепляли рейтинг!', message_thread_id= message.message_thread_id)
			return 0
		markup = types.InlineKeyboardMarkup()
		for rating in ratings_list:
			markup.add(types.InlineKeyboardButton(text=f"{rating[0]}", callback_data=f'achievements_stats|{rating[1]}'))
		bot.send_message(message.chat.id,"Выбор рейтинга", reply_markup=markup, message_thread_id=message.message_thread_id)
	except:
		bot.send_message(message.chat.id, 'вывести список прикрепленных рейтингов не удалось!', message_thread_id= message.message_thread_id)


#автоустановка простых еженедельных опросов
@bot.message_handler(commands=['set_auto_weekly_poll'])
def set_auto_weekly_poll(message):
    try:
        add_this_chat_if_not_exist(message.chat.id)
        chat_id = message.chat.id
        topic_id = 0 if message.message_thread_id is None else message.message_thread_id
        
        is_this_chat_have_auto_poll = fetch_one("SELECT poll_type FROM weekly_poll WHERE chat_id = ? AND topic_id = ?", (chat_id, topic_id))
        
        if not is_this_chat_have_auto_poll:
            simple_execute("INSERT INTO weekly_poll (chat_id, topic_id, poll_type) VALUES (?, ?, 'normal')", (chat_id, topic_id))
            bot.send_message(
                message.chat.id, 
                'Теперь в этом чате каждую неделю будут создаваться обычные опросы на игру!', 
                message_thread_id=message.message_thread_id
            )
        elif is_this_chat_have_auto_poll[0] == "ex":
            # ИСПРАВЛЕНО: меняем с ex на normal
            simple_execute("UPDATE weekly_poll SET poll_type = 'normal' WHERE chat_id = ? AND topic_id = ?", (chat_id, topic_id))
            bot.send_message(
                message.chat.id, 
                'Тип опроса изменен с "расширенного" на "обычный"', 
                message_thread_id=message.message_thread_id
            )
        elif is_this_chat_have_auto_poll[0] == 'normal':
            simple_execute("DELETE FROM weekly_poll WHERE chat_id = ? AND topic_id = ?", (chat_id, topic_id))
            bot.send_message(
                message.chat.id, 
                'Опросы отключены!', 
                message_thread_id=message.message_thread_id
            )
    except Exception as e:
        print(f"Ошибка в set_auto_weekly_poll: {e}")
        bot.send_message(
            message.chat.id, 
            'Не удалось настроить автоматическую рассылку!', 
            message_thread_id=message.message_thread_id
        )


#автоустановка расширенных еженедельных опросов
@bot.message_handler(commands=['set_auto_weekly_poll_ex'])
def set_auto_weekly_poll_ex(message):
    try:
        add_this_chat_if_not_exist(message.chat.id)
        chat_id = message.chat.id
        topic_id = 0 if message.message_thread_id is None else message.message_thread_id
        
        is_this_chat_have_auto_poll = fetch_one("SELECT poll_type FROM weekly_poll WHERE chat_id = ? AND topic_id = ?", (chat_id, topic_id))
        
        if not is_this_chat_have_auto_poll:
            simple_execute("INSERT INTO weekly_poll (chat_id, topic_id, poll_type) VALUES (?, ?, 'ex')", (chat_id, topic_id))
            bot.send_message(
                message.chat.id, 
                'Теперь в этом чате каждую неделю будут создаваться расширенные опросы на игру!', 
                message_thread_id=message.message_thread_id
            )
        elif is_this_chat_have_auto_poll[0] == "normal":
            # ИСПРАВЛЕНО: меняем с normal на ex
            simple_execute("UPDATE weekly_poll SET poll_type = 'ex' WHERE chat_id = ? AND topic_id = ?", (chat_id, topic_id))
            bot.send_message(
                message.chat.id, 
                'Тип опроса изменен с "обычного" на "расширенный"', 
                message_thread_id=message.message_thread_id
            )
        elif is_this_chat_have_auto_poll[0] == 'ex':
            simple_execute("DELETE FROM weekly_poll WHERE chat_id = ? AND topic_id = ?", (chat_id, topic_id))
            bot.send_message(
                message.chat.id, 
                'Опросы отключены!', 
                message_thread_id=message.message_thread_id
            )
    except Exception as e:
        print(f"Ошибка в set_auto_weekly_poll_ex: {e}")
        bot.send_message(
            message.chat.id, 
            'Не удалось настроить автоматическую рассылку!', 
            message_thread_id=message.message_thread_id
        )
#Коллбеки
@bot.callback_query_handler(func = lambda callback:True)
def answer(callback):
	callback_str = callback.data.split('|')
	if callback_str[0] == "show_rating_table":
		rating_table = rating_parser(callback_str[1], callback_str[2], callback_str[3])
		bot.send_message(callback.message.chat.id, rating_table, message_thread_id= callback.message.message_thread_id)
		return 0
	if callback_str[0] == "delete_rating_table":
		try:
			simple_execute("DELETE FROM links WHERE chat_id = ? AND pantheon_id = ?", (callback_str[1], callback_str[2]))
			bot.send_message(callback.message.chat.id, 'Ссылка на рейтинг удалена!', message_thread_id= callback.message.message_thread_id)
		except:
			bot.send_message(callback.message.chat.id, 'Не удалось удалить ссылку!', message_thread_id= callback.message.message_thread_id)
		return 0
	if callback_str[0] == "yaku_stats":
		bot.send_message(callback.message.chat.id, 'обработка началась. Это может занять время...', message_thread_id= callback.message.message_thread_id)
		yaku_statistic = yaku_stat(callback_str[1])
		bot.send_message(callback.message.chat.id, yaku_statistic, message_thread_id= callback.message.message_thread_id)
		return 0
	if callback_str[0] == "achievements_stats":
		yaku_statistic = achievements(callback_str[1])
		bot.send_message(callback.message.chat.id, yaku_statistic, message_thread_id= callback.message.message_thread_id)
		return 0
	if callback_str[0] == "rating_table_settings":
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton(text=f"Сортировать по рейтингу", callback_data=f'change_sort_rating_settings|rating|{callback_str[1]}|{callback_str[2]}'))
		markup.add(types.InlineKeyboardButton(text=f"Сортировать по ср. очкам", callback_data=f'change_sort_rating_settings|avg_score|{callback_str[1]}|{callback_str[2]}'))
		markup.add(types.InlineKeyboardButton(text=f"Сортировать по ср. месту", callback_data=f'change_sort_rating_settings|avg_place|{callback_str[1]}|{callback_str[2]}'))
		markup.add(types.InlineKeyboardButton(text=f"Фильтровать по всем игрокам", callback_data=f'change_filter_rating_settings||{callback_str[1]}|{callback_str[2]}'))
		markup.add(types.InlineKeyboardButton(text=f"Фильтровать по минимуму игр", callback_data=f'change_filter_rating_settings|min|{callback_str[1]}|{callback_str[2]}'))
		bot.send_message(callback.message.chat.id,"Выбор параметров", reply_markup=markup, message_thread_id=callback.message.message_thread_id)
		return 0
	if callback_str[0] == 'change_sort_rating_settings':
		simple_execute("UPDATE links SET pantheon_sorting = ? WHERE chat_id = ? AND pantheon_id = ?", (callback_str[1], callback_str[2], callback_str[3]))
		bot.send_message(callback.message.chat.id, f'Теперь таблица сортируется по {callback_str[1]}!', message_thread_id= callback.message.message_thread_id)
	if callback_str[0] == 'change_filter_rating_settings':
		simple_execute("UPDATE links SET pantheon_filter = ? WHERE chat_id = ? AND pantheon_id = ?", (callback_str[1], callback_str[2], callback_str[3]))
		bot.send_message(callback.message.chat.id, f'Теперь таблица фильтруется {"по минимуму игр" if callback_str[1] == "min" else "по всем игрокам"}!', message_thread_id= callback.message.message_thread_id)


#вывод списка команд
@bot.message_handler(commands=['help', 'commands', 'command', 'MEDIC', 'DOCTOR', 'MEDIC_CHARGE_ME', 'DOCTOR_CHARGE_ME'])
def help(message):
	bot.send_message(message.chat.id, help_info, message_thread_id= message.message_thread_id)
#запуск бота
bot.polling(none_stop = True)