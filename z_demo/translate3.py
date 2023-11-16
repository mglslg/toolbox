# coding = utf-8
import requests
from bs4 import BeautifulSoup


def trans():
    url = 'http://dict.youdao.com/search?q=good&keyfrom=new-fanyi.smartResult'
    html = requests.post(url).content
    html_doc = str(html, 'utf-8')  # html_doc=html.decode("utf-8","ignore")
    print(html_doc)


def scratch():
    url = 'http://dict.youdao.com/search?q=good&keyfrom=new-fanyi.smartResult'
    html = requests.post(url).content
    content = str(html, 'utf-8')
    soup = BeautifulSoup(content, 'lxml')
    translated = soup.find('div', {"class": "trans-container"}).findAll('li')
    for x in translated:
        print(x.text)


if __name__ == '__main__':
    scratch()
