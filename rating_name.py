import requests
from bs4 import BeautifulSoup
import fake_useragent
user = fake_useragent.UserAgent().random
header = {"user-agent": user}
def rating_name(a):
    try:
        link = a
        responce = requests.get(link, headers=header).text
        soup = BeautifulSoup(responce, "lxml")
        main = soup.find("main", class_="m_8983817 mantine-AppShell-main")
        h2 = main.find("h2")
        return h2.text[:-15]
    except:
        return link