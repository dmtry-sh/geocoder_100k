import requests
from bs4 import BeautifulSoup


class Proxy(object):

    proxy_url = 'http://www.ip-adress.com/proxy_list/'
    proxy_list = []

    # при инициализации класса создаётся список анонимных прокси серверов
    def __init__(self):
        r = requests.get(self.proxy_url)
        soup = BeautifulSoup(r.content.decode('utf-8'), 'lxml')
        table = soup.find('table', class_='htable').find('tbody').find_all('tr')
        result = [n.find_all('td') for n in table]
        result = [{'ip': n[0].text, 'anonymous': n[1].text, 'used': False} for n in result]
        result = [n for n in result if n['anonymous'] == 'anonymous' or n['anonymous'] == 'highly-anonymous']
        self.proxy_list = result
    
    # если соединение с сервером хорошее, возвращает url сервера
    # помечает сервер как использованный
    def get_proxy(self):
        for proxy in self.proxy_list:
            url = 'http://' + proxy['ip']
            try:
                r = requests.get('http://ya.ru', proxies={'http': url})
                if r.status_code == 200:
                    proxy['used'] = True
                    return url
            except requests.exceptions.ConnectionError:
                continue

    # обновляет список серверов
    def update_proxy(self):
        r = requests.get(self.proxy_url)
        soup = BeautifulSoup(r.content.decode('utf-8'), 'lxml')
        table = soup.find('table', class_='htable').find('tbody').find_all('tr')
        result = [n.find_all('td') for n in table]
        result = [{'ip': n[0].text, 'anonymous': n[1].text} for n in result]
        result = [n for n in result if n['anonymous'] == 'anonymous' or n['anonymous'] == 'highly-anonymous']
        self.proxy_list = result

    # возвращает следующий работающий сервер или ничего
    def next_server(self):
        for proxy in self.proxy_list:
            if proxy['used'] == False:
                url = 'http://' + proxy['ip']
                try:
                    r = requests.get('http://ya.ru', proxies={'http': url})
                    if r.status_code == 200:
                        proxy['used'] = True
                        return url
                except requests.exceptions.ConnectionError:
                    continue
            else:
                continue
        return None

#proxy = Proxy()
#proxy_ip = proxy.get_proxy()
#for i in range(20):
#    print(i + 1, proxy_ip)
#    proxy_ip = proxy.next_server()