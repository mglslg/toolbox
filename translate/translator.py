import requests
from bs4 import BeautifulSoup
import json
from prettytable import PrettyTable
import textwrap


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

    if len(result) > 0:
        return json.dumps(result, ensure_ascii=False), json.dumps(voice, ensure_ascii=False), json.dumps(exp,
                                                                                                         ensure_ascii=False)
    else:
        return [], [], []


def trans_to_list(__word):
    __rs = translate(__word)
    if len(__rs) != 0:
        __word = json.loads(str(__rs[0]).replace("'", "\""))
        __voice = json.loads(__rs[1])
        __eg = json.loads(__rs[2])
        return __word, __voice, __eg


def trans_to_format(word):
    __rs = trans_to_list(word)
    if len(__rs[0]) == 0:
        return None
    word = '\n'.join(__rs[0])
    voice = '\n'.join(__rs[1])
    eg = '\n'.join(__rs[2])
    table = PrettyTable(['单词', '音标'])
    table.add_row([word, voice])
    return table, eg


def main():
    while True:
        w = input("请输入单词:")
        if w == 'quit' or w == 'exit':
            return
        __rs = trans_to_format(w)
        if not __rs:
            print('查无此词!')
        else:
            print(__rs[0])
            print(__rs[1])


if __name__ == '__main__':
    rs = trans_to_format("good")
    print(rs)
