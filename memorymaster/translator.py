import requests
from bs4 import BeautifulSoup


def translate(word):
    result = []
    voice = []
    url = 'http://dict.youdao.com/search'
    data = {
        'q': word,
        'keyfrom': 'new-fanyi.smartResult'
    }
    html = requests.post(url, data=data).content
    content = str(html, 'utf-8')
    soup = BeautifulSoup(content, 'lxml')
    trans_container = soup.find('div', {"class": "trans-container"})
    phonetic_container = soup.find('div', {"id": "phrsListTab"})

    if trans_container is None:
        return result

    translated = trans_container.findAll('li')
    for x in translated:
        result.append(x.text)

    phonetic = phonetic_container.findAll('span', {"class": "phonetic"})
    for y in phonetic:
        voice.append(y.text)

    return result, voice


if __name__ == '__main__':
    rs = translate('task')
    print(rs)
    if len(rs) != 0:
        print(rs[0])
