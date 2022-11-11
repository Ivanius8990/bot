import time
import concurrent.futures

from bot_v2_fonbet import bot_v2_fonbet
from bot_v2_marafon import bot_v2_marafon
from settings import *


def ran_parse(setting):
    bot_name=setting['bot_name']
    url=setting['url']
    while True:
        try:
            print("Запускаю парсинг "+bot_name)
            globals()[bot_name](url)
            print("Парсинг "+bot_name+ " окончен")
        except:
            handle_crash(setting)
        time.sleep(60*5)

def handle_crash(setting):
    bot_name = setting['bot_name']
    print("Произошла ошибка в "+bot_name+"\nБудет произведен перезапуск")
    time.sleep(2)  # Restarts the script after 2 seconds
    ran_parse(setting)


###потоки
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for setting in settings:
        futures.append(executor.submit(ran_parse, setting=setting))
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
