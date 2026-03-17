import requests
from bs4 import BeautifulSoup
import fake_useragent
user = fake_useragent.UserAgent().random
header = {"user-agent": user}
def get_rating_name(pantheon_id):
    try:
        rating_link = f'https://rating.riichimahjong.org/event/{pantheon_id}/order/rating'
        response = requests.get(rating_link, headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")
        main = soup.find("main", class_="m_8983817 mantine-AppShell-main")
        h2 = main.find("h2")
        return h2.text[:-15]
    except:
        return rating_link
