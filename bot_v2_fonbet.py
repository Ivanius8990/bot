import re
import time
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric, delete, insert
from selenium import webdriver
from selenium.webdriver import ActionChains, Proxy
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from proxy import prox

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
s = Service('C:\webdriver\chromedriver.exe')

def bot_v2_fonbet(url):
    ### настройки прокси
    proxy_url =prox()
    proxy = Proxy({
        'proxyType': 'MANUAL',
        'httpProxy': proxy_url,
        'sslProxy': proxy_url,
        'noProxy': ''})
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(ChromeDriverManager().install(),desired_capabilities=capabilities)


    # url = 'https://www.fon.bet/sports/esports/'

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
        target = target[-1]
        scroll_origin = ScrollOrigin.from_element(target)
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, 176).perform()

    driver.close()
    driver.quit()

    sep = 'ИТОГИ'
    text = file.split(sep, 1)[0]

    teams_and_kef = re.findall(
        r"([\w'.-]+[ ]?[\w'.-]*[ ]?[\w'.-]*)\s—\s([\w'.]+[ ]?[\w'.-]*[ ]?[\w'.-]*)\s[\d\w :]*\s(\d+[.]\d*)\s[-]?\s?(\d+[.]\d*)",
        text)


    table = []
    for i in range(len(teams_and_kef)):
        xx = {
            'first_team': teams_and_kef[i][0].upper(),
            'second_team': teams_and_kef[i][1].upper(),
            'kef1': teams_and_kef[i][2],
            'kef2': teams_and_kef[i][3]
        }
        if xx not in table:
            table.append(xx)
            print(teams_and_kef[i][0], teams_and_kef[i][1], teams_and_kef[i][2], teams_and_kef[i][3])

    engine = create_engine("postgresql+psycopg2://postgres:1234567@localhost/stavki")
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

    print(f'Всего найдено {r.rowcount} матчей\n')
