#Парсер рейтинга с сайта пантеон
import requests
from bs4 import BeautifulSoup
import fake_useragent
user = fake_useragent.UserAgent().random
header = {"user-agent": user}
def rating_parser(a, sort, filter):
	try:
		link = a
		if sort =="":
			link = a
		elif sort == "avg_score":
			link = link.replace("order/rating", "order/avg_score")
		elif sort =="avg_place":
			link = link.replace("order/rating", "order/avg_place")
		if filter =="min":
			link +="/filter/min"
		responce = requests.get(link, headers = header).text
		soup = BeautifulSoup(responce, "lxml")
		#парсинг таблицы
		root = soup.find('div', id = "root")
		main = root.find('div', class_="m_89ab340 mantine-AppShell-root")
		main2 = main.find("main", class_="m_8983817 mantine-AppShell-main")
		main3 = main2.find('div', class_="m_7485cace mantine-Container-root")
		last_n = len(main3.find_all('div', class_="m_4081bf90 mantine-Group-root"))
		ans = ''
		for i in range(2, last_n,2):
			#поиск имя
			main4 = main3.find_all('div', class_="m_4081bf90 mantine-Group-root")[i]
			main5 = main4.find('div', class_="m_6d731127 mantine-Stack-root")
			main6 = main5.find('a').text
			if sort =="avg_score":
				main7 = main3.find_all('div', class_="m_4081bf90 mantine-Group-root")[i + 1]
				main8 = main7.find_all("div", class_="m_347db0ec mantine-Badge-root")[1]
				main9 = main8.find('span', class_="m_5add502a mantine-Badge-label").text
				games = main7.find_all("div", class_="m_347db0ec mantine-Badge-root")[3]
				games = games.find('span', class_="m_5add502a mantine-Badge-label").text
				ans += f"{i // 2}){main6}. Счёт {main9}. Игр {games}\n"
			elif sort =="avg_place":
				main7 = main3.find_all('div', class_="m_4081bf90 mantine-Group-root")[i + 1]
				main8 = main7.find_all("div", class_="m_347db0ec mantine-Badge-root")[2]
				main9 = main8.find('span', class_="m_5add502a mantine-Badge-label").text
				games = main7.find_all("div", class_="m_347db0ec mantine-Badge-root")[3]
				games = games.find('span', class_="m_5add502a mantine-Badge-label").text
				ans += f"{i // 2}){main6}. Место {main9}. Игр {games}\n"
			else:
				#поиск рейтинга
				main7 = main3.find_all('div', class_="m_4081bf90 mantine-Group-root")[i+1]
				main8 = main7.find("div", class_="m_347db0ec mantine-Badge-root")
				main9 = main8.find('span',class_="m_5add502a mantine-Badge-label").text
				games = main7.find_all("div", class_="m_347db0ec mantine-Badge-root")[3]
				games = games.find('span', class_="m_5add502a mantine-Badge-label").text
				ans += f"{i//2}){main6}. Рейтинг {main9}. Игр {games}\n"
		if ans !="":
			return ans
		else:
			return "таблица пуста"
	except:
		return 'ОШИБКА! Считать таблицу не удалось. Проверьте, как вы прикрепили ссылку, команда должна выглядеть вот так - /rating_link ваша_ссылка'