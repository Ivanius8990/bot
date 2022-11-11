from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric, delete, insert
import time
from selenium import webdriver
from selenium.webdriver import ActionChains, Proxy
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from proxy import prox

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")

### настройки прокси
proxy_url =prox()
proxy = Proxy({
    'proxyType': 'MANUAL',
    'httpProxy': proxy_url,
    'sslProxy': proxy_url,
    'noProxy': ''})
capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

driver = webdriver.Chrome(executable_path='/home/vanya7000i/.wdm/drivers/chromedriver/linux64/107.0.5304/chromedriver',chrome_options=chrome_options,desired_capabilities=capabilities)

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

driver.close()
driver.quit()

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

engine = create_engine("postgresql+psycopg2://mrsmith:Flatron700?@localhost/stavki")
metadata = MetaData()
marafon = Table('marafon', metadata,
                Column('id', Integer(), primary_key=True),
                Column('first_team', String(100), nullable=False),
                Column('second_team', String(100), nullable=False),
                Column('kef1', Numeric(8, 5), nullable=False),
                Column('kef2', Numeric(8, 5), nullable=False)
                )

metadata.create_all(engine)
conn = engine.connect()
conn.execute('TRUNCATE TABLE marafon RESTART IDENTITY;')
ins = insert(marafon)
r = conn.execute(ins, table)

print(f'Всего найдено {r.rowcount} матчей')
