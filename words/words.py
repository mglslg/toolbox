import json
import re
import os
import requests

# print(os.path.abspath("."))
_data_file = os.getcwd() + '/words_data.txt'


def add():
    print("请输入英文:")
    en = input()
    print("请输入中文:")
    cn = input()
    data = {
        'en': en,
        'cn': cn,
        'tags': []
    }
    with open(_data_file, 'at', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')


def ls():
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            currData = json.loads(line)
            print(currData['cn'])


def ls_word(word):
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            currData = json.loads(line)
            if currData['en'] == word:
                return currData


while True:
    string = str(input("请输入一段要翻译的文字："))
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'smartresult' : 'dict',
        'i': string
    }
    url = "http://fanyi.youdao.com/translate"
    # url = "http://fanyi.youdao.com/translate_o"
    r = requests.get(url, params=data)
    result = r.json()
    print(result)

    cmd = input(">>> ")
    if cmd == 'exit':
        break
    if cmd == 'add':
        add()
    elif cmd == 'ls':
        ls()
    else:
        w_match = re.search("ls -w\\s+\\w+", cmd)
        if w_match:
            results = re.split("\\s+", cmd)
            print(len(results))
            if len(results) != 3:
                print("param error")
            else:
                target_word = results[2]
                print(target_word)
        else:
            print("command not found: " + cmd)
