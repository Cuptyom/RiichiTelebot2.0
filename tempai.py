from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time

def tempai_eff(hand):
    ws = ["東", "南", "西", "北"]
    try:
        hand = hand.split("/")
        dora = hand[3]
        doras = [dora[i] + dora[i+1] for i in range(0, len(dora), 2)]
        round_w = hand[1]
        sit_w = hand[2]
        hand = hand[0]
    except:
        return (
            "введите все параметры:\n"
            "p123m456s7z1234567/ветер раунда (0-восток, 3 - север)/"
            "ветер места(аналогично)/индикаторы дор (s1p2z3)\n"
            "пример: p123456789s194z12/3/2/s1z2"
        )

    # Настройка Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Обязательно для сервера
    options.add_argument("--no-sandbox")  # Обязательно для Timeweb
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={UserAgent().random}")
    
    # Запуск через webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://kobalab.net/majiang/dapai.html"
        driver.get(url)

        if sum(c.isdigit() for c in hand) != 14:
            return "неверное количество тайлов"

        # Ввод руки
        hand_input = driver.find_element(By.NAME, "paistr")
        hand_input.clear()
        hand_input.send_keys(hand)

        # Ввод дор
        dora_inputs = driver.find_elements(By.NAME, "baopai")
        for i, d in enumerate(doras):
            if i < len(dora_inputs):
                dora_inputs[i].clear()
                dora_inputs[i].send_keys(d)

        # Ветер раунда
        driver.find_element(By.NAME, "zhuangfeng").click()
        driver.find_element(By.XPATH, f"//*[text()='{ws[int(round_w)]}']").click()

        # Ветер места
        driver.find_element(By.NAME, "menfeng").click()
        driver.find_element(By.XPATH, f"//*[text()='{ws[int(sit_w)]}']").click()

        # Отправка формы
        hand_input.send_keys(Keys.ENTER)

        time.sleep(1)  # чуть-чуть подождать для подгрузки

        tiles = driver.find_elements(By.CLASS_NAME, "row")
        answer = ""
        for i in tiles:
            answer += "сброс " + str(i.get_attribute("data-dapai")) + " ожидания: "
            waits = i.find_elements(By.CLASS_NAME, "pai")
            for j in waits[1:]:
                answer += j.get_attribute("data-pai") + " "
            answer += "\n"

        if "None" not in answer:
            return (
                answer.replace("z1", "восток").replace("z2", "юг")
                      .replace("z3", "запад").replace("z4", "север")
                      .replace("z5", "белый").replace("z6", "зеленый")
                      .replace("z7", "красный")
            )
        else:
            return "ожиданий нет (рука темпай или введена неверно)"
    finally:
        driver.quit()
