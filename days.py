#модуль для опросов недели
from datetime import *

#функция для фомирования массива вариантов ответов на эту неделю
def this_week():
	data = datetime.now() - timedelta(days = datetime.now().weekday() + 1)
	n = []
	for i in range(7):
		data = data + timedelta(days = 1)
		n += [f'{data.day}.{data.month} - {week_day(data)}']
	n += ['я не смогу', 'играю не все дни']
	return n

#функция для фомирования массива вариантов ответов на следующую неделю
def next_week():
	data = datetime.now() - timedelta(days = datetime.now().weekday() - 6)
	n = []
	for i in range(7):
		data = data + timedelta(days = 1)
		n += [f'{data.day}.{data.month} - {week_day(data)}']
	n += ['я не смогу', 'играю не все дни']
	return n

#функция для перевода дней недели на русский
def week_day(data):
	a = data.weekday()
	names = ["Понедельник", "Вторник", 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
	for i in names:
		if names.index(i) == a:
			a = names[names.index(i)]
			break
	return a
# функции next_week и this_week() возвращают массив строк.
#['16.3 - Понедельник', '17.3 - Вторник', '18.3 - Среда', '19.3 - Четверг', '20.3 - Пятница', '21.3 - Суббота', '22.3 - Воскресенье', 'я не смогу', 'играю не все дни']

#код для бота
#@bot.message_handler(commands=['this_week_poll'])
#def this_week_poll(message):
#    bot.send_poll(message.chat.id, 'Играем?', this_week(), is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)
# опрос след. недели
#@bot.message_handler(commands=['next_week_poll'])
#def this_week_poll(message):
#	bot.send_poll(message.chat.id, 'Играем?', next_week(), is_anonymous = False, allows_multiple_answers = True, message_thread_id= message.message_thread_id)