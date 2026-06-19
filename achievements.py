#Парсер ачивок
import time
import requests
from bs4 import BeautifulSoup
import fake_useragent
user = fake_useragent.UserAgent().random
header = {"user-agent": user}

def achievements(getted_id):
	link = f'https://rating.riichimahjong.org/event/{getted_id}/achievements'
	responce = requests.get(link, headers = header).text
	soup = BeautifulSoup(responce, "lxml")

	achieve_box = soup.find("div", class_ = 'm_9bdbb667 mantine-Accordion-root')

	achievements_list = achieve_box.find_all("div", class_='m_1f921b3b m_9bd7b098 mantine-Accordion-item')

	a = []

	blank = "no info"

	for i in achievements_list:
		#ищем имя 
		try:
			achievement_name = i.find_all("p", class_="mantine-focus-auto m_b6d8b162 mantine-Text-root")
		except:
			achievement_name = blank

		try:
			achieve_player = i.find_all("span", class_="mantine-List-itemLabel")
		except:
			achieve_player = blank
		try:
			achieve_value = i.find_all("span", class_="m_5add502a mantine-Badge-label")
		except:
			achieve_value = blank

		for i in achievement_name:
			print(i.text)
		for i in achieve_player[:3]:
			print(i.text)
		for i in achieve_value[:3]:
			print(i.text)
		#print(achievement_name, achieve_player, achieve_value)
	#return achievement_name, achieve_player, achieve_value

achievements(875)
#print(achievements(875))