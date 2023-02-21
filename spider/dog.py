import requests
from config import url
from bs4 import BeautifulSoup

def dog(url):
    data = requests.get(url)
    data.encoding = 'utf-8'
    html = data.text
    print(html)

    return
if __name__ == '__main__':
    d = dog(url)

