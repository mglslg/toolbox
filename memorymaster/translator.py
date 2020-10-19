import requests
from bs4 import BeautifulSoup
import json


def translate(word):
    result = []
    voice = []
    exp = []
    url = 'http://dict.youdao.com/search'
    data = {
        'q': word,
        'keyfrom': 'new-fanyi.smartResult'
    }
    html = requests.post(url, data=data).content
    content = str(html, 'utf-8')
    # print(content)
    soup = BeautifulSoup(content, 'lxml')
    trans_container = soup.find('div', {"class": "trans-container"})
    phonetic_container = soup.find('div', {"id": "phrsListTab"})
    collins_result = soup.find('div', {"id": "collinsResult"})

    if trans_container is None:
        return result

    translated = trans_container.findAll('li')
    for x in translated:
        result.append(x.text)

    phonetic = phonetic_container.findAll('span', {"class": "phonetic"})
    for y in phonetic:
        voice.append(y.text)

    if collins_result is not None:
        examples = collins_result.findAll('div', {"class": "examples"})
        for e in examples:
            exp.append(e.text)
            if exp.__len__() > 4:
                break

    return json.dumps(result, ensure_ascii=False), json.dumps(voice, ensure_ascii=False), json.dumps(exp,
                                                                                                     ensure_ascii=False)


if __name__ == '__main__':
    rs = translate('abandon')
    if len(rs) != 0:
        print(str(rs[0]).replace("'", "\""))
        print(rs[1])
        print(rs[2])
