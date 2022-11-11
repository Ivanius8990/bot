import requests
import random
from bs4 import BeautifulSoup as bs
import re

def get_session(proxies):
    print('.', end='')
    # создать HTTP‑сеанс
    session = requests.Session()
    # выбираем один случайный прокси
    proxy = random.choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}
    s=session.get("http://icanhazip.com", timeout=1.5).text.strip()
    port= proxy.split(':')[1]
    prox = re.findall(r"\d+\.\d+\.\d+\.\d+", s)
    if len(prox)>0:
        return prox,port


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"class": "table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


def prox():
    try:
        free_proxies = get_free_proxies()
        x,y = get_session(free_proxies)
        if x!= None:
            ip= (x[0]+":"+y)
            print('\nПрокси найден\nIP : ',ip)
            return ip
        else:
            prox()
    except Exception:
        prox()



if __name__ == '__main__':
    prox()