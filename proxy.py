import requests
from lxml import html


class Proxy(object):

    proxy_url = 'http://www.ip-adress.com/proxy_list/'
    proxy_list = []

    def __init__(self):
        r = requests.get(self.proxy_url)
        str = html.fromstring(r.content)
        result = str.xpath("//tr[@class='odd']/td[1]/text()")
        self.proxy_list = result
    
    def get_proxy(self):
        for proxy in self.proxy_list:
            url = 'http://' + proxy
            try:
                r = requests.get('http://ya.ru', proxies={'http': url})
                if r.status_code == 200:
                    return url
            except requests.exceptions.ConnectionError:
                continue

proxy = Proxy()
proxy = proxy.get_proxy()
print(proxy)
