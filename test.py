import re
import time
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric, delete, insert
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

s = Service('C:\webdriver\chromedriver.exe')
url = 'https://www.marathonbet.ru/su/popular/e-Sports+-+1895085'

driver.get(url)
wait = WebDriverWait(driver, 10)  ###все wait ждут пока загрузится элемент
wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))

time.sleep(2.5)
iframe = driver.find_element(By.TAG_NAME, "footer")
ActionChains(driver) \
    .scroll_to_element(iframe) \
    .perform()

file = []
time.sleep(2.5)
body = driver.find_element(By.TAG_NAME, 'body').text

with open("file.txt", "w", encoding="utf-8") as output:
    output.write(str(body))

body = body.encode()
body = body.decode('utf-8')
team1 = re.findall(r"1\.\s([\w.-]+[ ]?[\w.-]*[ ]?[\w.-]*)\b", body)
team2 = re.findall(r"2\.[\n]+([\w.-]+[ ]?[\w.-]*[ ]?[\w.-]*)\b", body)
kef = re.findall(r"(\d*[.]\d*)[ ](\d*[.]\d*)", body)

table = []
min_range=min(len(team1),len(team2),len(kef))
for i in range(min_range):
    print(team1[i], team2[i], kef[i][0], kef[i][1])
    xx = {
        'first_team': team1[i],
        'second_team': team2[i],
        'kef1': kef[i][0],
        'kef2': kef[i][1]
    }
    table.append(xx)

