import requests
from bs4 import BeautifulSoup


def translate(word):
    url = 'http://dict.youdao.com/search'
    data = {
        'q': word,
        'keyfrom': 'new-fanyi.smartResult'
    }
    html = requests.post(url, data=data).content
    content = str(html, 'utf-8')
    soup = BeautifulSoup(content, 'lxml')
    translated = soup.find('div', {"class": "trans-container"}).findAll('li')
    result = []
    for x in translated:
        result.append(x.text)

    return result


if __name__ == '__main__':
    rs = translate('translate')
    print(rs[0])
