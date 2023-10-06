import requests
import random
from bs4 import BeautifulSoup
from ..site_tags import tags

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]


class ByUserRequest:
    def __init__(self, url):
        self.url = url
        self.attributes = tags

    def recognizer(self):
        """
        Функция «Распознаватель» проверяет, соответствует ли данный URL-адрес каким-либо ключам в словаре атрибутов, и
        возвращает соответствующие атрибуты, если они найдены, или сообщение, указывающее, что сайт не найден.

        :return:
            словарь с двумя парами ключ-значение. Ключ «url» связан со значением self.url,
            а ключ «attributes» связан со значением self.attributes[urlkey].
            Если URL-ключ не найден в URL-адресе, значением атрибутов будет «Сайт не найден!».
        """
        print('self.url: ', self.url)
        for urlkey in self.attributes.keys():
            if urlkey in self.url:
                return {"url": self.url, "attributes": self.attributes[urlkey]}
            else:
                return {"url": self.url, "attributes": "Site not found !"}

    def getting_price(self):
        """
        Функция getting_price получает цену продукта с веб-сайта с помощью BeautifulSoup и возвращает ее в виде строки.

        :return:
            Код возвращает цену продукта, если он найден на веб-странице.
            Если цена не найдена, возвращается строка «Цена не найдена!».
        """
        getting_tags = self.recognizer()
        print('getting_tags: ', getting_tags)
        resp = requests.get(getting_tags["url"], headers={'User-Agent': random.choice(user_agents)})
        soup = BeautifulSoup(resp.content, "lxml")

        for key, item in getting_tags["attributes"].items():
            try:
                price = soup.find(item[0], class_=item[-1]).text.strip().encode("ascii", "ignore").decode()
            except AttributeError:
                return "Price not found!"
            else:
                return price