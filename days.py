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

#текущая дата со смещением
def this_day(step = 0):
    date = datetime.now() - timedelta(days = datetime.now().weekday() - step)
    date = f'{date.day}.{date.month} - {week_day(date)}'
    poll_info = [date, 'Смогу играть весь день!', 'Смогу только днём!', 'Смогу только вечером!', 'Возможно смогу, но не точно!', 'Точно не смогу!']
    return poll_info

#функция для перевода дней недели на русский
def week_day(data):
	a = data.weekday()
	names = ["Понедельник", "Вторник", 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
	for i in names:
		if names.index(i) == a:
			a = names[names.index(i)]
			break
	return a