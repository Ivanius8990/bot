from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric, delete, insert
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import re
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")

driver = webdriver.Chrome(executable_path='/home/vanya7000i/.wdm/drivers/chromedriver/linux64/107.0.5304/chromedriver',chrome_options=chrome_options)

url = 'https://www.fon.bet/sports/esports/'

driver.get(url)
time.sleep(2.5)

file = ''

def target_find():
    target = driver.find_elements(By.CSS_SELECTOR, "div[class^='sport-event-separator']")
    if len(target)==0:
        return False
    else:
        return target

for i in range(50):
    while not target_find():
        target_find()
    target= target_find()
    body = driver.find_element(By.TAG_NAME, 'body').text
    file += body
    target = target[-2]
    scroll_origin = ScrollOrigin.from_element(target)
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, 176).perform()

driver.close()
driver.quit()

sep = 'ИТОГИ'
text = file.split(sep, 1)[0]

teams_and_kef = re.findall(
    r"([\w.-]+[ ]?[\w.-]*[ ]?[\w.-]*)\s—\s([\w.]+[ ]?[\w.-]*[ ]?[\w.-]*)\s[\d\w :]*\s(\d+[.]\d*)\s[-]?\s?(\d+[.]\d*)",
    text)

table = []
for i in range(len(teams_and_kef)):
    xx = {
        'first_team': teams_and_kef[i][0],
        'second_team': teams_and_kef[i][1],
        'kef1': teams_and_kef[i][2],
        'kef2': teams_and_kef[i][3]
    }
    if xx not in table:
        table.append(xx)
        print(teams_and_kef[i][0], teams_and_kef[i][1], teams_and_kef[i][2], teams_and_kef[i][3])

engine = create_engine("postgresql+psycopg2://mrsmith:Flatron700?@localhost/stavki")
metadata = MetaData()
fonbet = Table('fonbet', metadata,
               Column('id', Integer(), primary_key=True),
               Column('first_team', String(100), nullable=False),
               Column('second_team', String(100), nullable=False),
               Column('kef1', Numeric(8, 5), nullable=False),
               Column('kef2', Numeric(8, 5), nullable=False)
               )

metadata.create_all(engine)
conn = engine.connect()
r = conn.execute('TRUNCATE TABLE fonbet RESTART IDENTITY;')
ins = insert(fonbet)
r = conn.execute(ins, table)

print(f'Всего найдено {r.rowcount} матчей')
