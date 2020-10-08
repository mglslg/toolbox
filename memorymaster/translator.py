import requests
from bs4 import BeautifulSoup


def translate(word):
    result = []
    url = 'http://dict.youdao.com/search'
    data = {
        'q': word,
        'keyfrom': 'new-fanyi.smartResult'
    }
    html = requests.post(url, data=data).content
    content = str(html, 'utf-8')
    soup = BeautifulSoup(content, 'lxml')
    trans_container = soup.find('div', {"class": "trans-container"})

    if trans_container is None:
        return result

    translated = trans_container.findAll('li')
    for x in translated:
        result.append(x.text)

    return result


if __name__ == '__main__':
    rs = translate('transladfsdfte')
    if len(rs) != 0:
        print(rs[0])

