#Парсер ачивок
import time
import requests
from bs4 import BeautifulSoup
import fake_useragent
def isfloat(number):
	try:
		return float(number)
	except:
		return False
def achievements(getted_id):
	try:
		user = fake_useragent.UserAgent().random
		header = {"user-agent": user}
		cookies = {"lng": "ru"}
		link = f'https://rating.riichimahjong.org/event/{getted_id}/achievements'
		responce = requests.get(link, headers = header, cookies=cookies)
		soup = BeautifulSoup(responce.text, "lxml")

		achieve_box = soup.find("div", class_ = 'm_9bdbb667 mantine-Accordion-root')
		answer = ''
		achievements_list = achieve_box.find_all("div", class_='m_1f921b3b m_9bd7b098 mantine-Accordion-item')
		for achieve in achievements_list:
			try:
				achieve_name = achieve.find_all('p', class_="mantine-focus-auto m_b6d8b162 mantine-Text-root")[0]
				achieve_desk = achieve.find_all('p', class_="mantine-focus-auto m_b6d8b162 mantine-Text-root")[1]
				achieve_players = achieve.find_all('span', class_='mantine-List-itemLabel')
				if len(achieve_players) == 0:
					continue
				achieve_value = achieve.find('span', class_='m_5add502a mantine-Badge-label')
				answer += f'{achieve_name.text}\n'
				answer += f'{achieve_desk.text}\n'
				if not achieve_value.text and len(achieve_players) > 0:
					try:
						max_val = [i for i in achieve_players[0].text.split() if i.isdigit() or isfloat(i)][0]
					except:
						max_val = None	
				for player in achieve_players:
					if not achieve_value.text and len(achieve_players) > 0 and max_val:
						value = [i for i in player.text.split() if i.isdigit() or isfloat(i)][0]
						if value == max_val:
							answer += f'{player.text}\n'
					else:
						answer += f'{player.text}\n'
				answer += f'{achieve_value.text}\n' if achieve_value.text else ''
				answer += '\n'
			except:
				answer += f'!!!READING ERROR!!!\n'
		return answer
	except:
		return "Получить статистику по достижениям не удалось!"
