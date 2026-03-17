#Парсер рейтинга с сайта пантеон
import time
import requests
from bs4 import BeautifulSoup
import fake_useragent
user = fake_useragent.UserAgent().random
header = {"user-agent": user}
yaku = [
    "Riichi","Ippatsu","Pinfu","Junchan","Sanshoku","Yakuhai x1","Yakuhai x4","Honroutou","Sankantsu","Rinshan kaihou","Suukantsu","Shousuushii","Chinroutou","Ryuuiisou",
    "Chihou","Daburu riichi","Menzentsumo","Tanyao","Iipeikou","Sanshoku doukou","Yakuhai x2","Toitoi","Sanankou","Houtei raoyui","Chankan","Suuankou","Daisuushii","Chinitsu",
    "Kokushi musou","Open riichi","Chiitoitsu","Chanta","Ryanpeikou","Ittsu","Yakuhai x3","Honitsu","Shousangen","Haitei","Renhou","Daisangen","Tsuuiisou","Chuuren poutou", "Tenhou"
        ]
def panteon_stat(getted_link):
    try:
        getted_id = getted_link[39:-13]
        link = f"https://rating.riichimahjong.org/event/{getted_id}/games/page/1"
        responce = requests.get(link, headers = header).text
        soup = BeautifulSoup(responce, "lxml")
        txt = soup.find_all("ul", class_="m_abbac491 mantine-List-root")
        num = soup.find_all("button", class_="mantine-focus-auto mantine-active m_326d024a mantine-Pagination-control m_87cf2631 mantine-UnstyledButton-root")
        if len(num) == 1:
            b = -1
        else:
            b = -2
        num = soup.find_all("button", class_="mantine-focus-auto mantine-active m_326d024a mantine-Pagination-control m_87cf2631 mantine-UnstyledButton-root")[b]
        num_of_page = num.text
        yaku_list = []
        for yaku_name in yaku:
            count_yaku = 0
            if yaku_name != "Riichi":
                for page in range(1, int(num_of_page)+1):
                    time.sleep(1)
                    link = f"https://rating.riichimahjong.org/event/{getted_id}/games/page/{page}"
                    responce = requests.get(link, headers = header).text
                    soup = BeautifulSoup(responce, "lxml")
                    txt = soup.find_all("ul", class_="m_abbac491 mantine-List-root")
                    for i in txt:
                        a = str(i.text)
                        count_yaku += a.count(yaku_name)
            else:
                for page in range(1, int(num_of_page) + 1):
                    time.sleep(1)
                    link = f"https://rating.riichimahjong.org/event/{getted_id}/games/page/{page}"
                    responce = requests.get(link, headers=header).text
                    soup = BeautifulSoup(responce, "lxml")
                    txt = soup.find_all("ul", class_="m_abbac491 mantine-List-root")
                    for i in txt:
                        a = str(i.text)
                        count_yaku += a.count(yaku_name) - a.count("Riichi bets")
            yaku_list+=[[count_yaku,yaku_name]]
        all_yaku = 0
        for page in range(1, int(num_of_page) + 1):
            link = f"https://rating.riichimahjong.org/event/{getted_id}/games/page/{page}"
            responce = requests.get(link, headers=header).text
            soup = BeautifulSoup(responce, "lxml")
            txt = soup.find_all("ul", class_="m_abbac491 mantine-List-root")
            for i in txt:
                a = str(i.text)
                all_yaku += a.count("東") + a.count("南")
        a = ''
        yaku_list = sorted(yaku_list, reverse = True)
        for i in yaku_list:
            if i[0]/all_yaku != 0:
                a += f"{i[1]}: {i[0]}, {round(i[0]/all_yaku * 100,2)}% \n"
        a += f'всего сыгранных раздач {all_yaku}'
        return a
    except:
        return 'ОШИБКА! Считать таблицу не удалось. Проверьте, как вы прикрепили ссылку, команда должна выглядеть вот так - /rating_link ваша_ссылка'