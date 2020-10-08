# coding = utf-8
import requests


def trans(str):
    url = 'http://fanyi.youdao.com/translate'
    payload = {'i': str,
               'action': 'FY_BY_REALTlME',
               'bv': 'a02d4a63adf2591ffe445a9fb4ea14dc',
               'client': 'fanyideskweb',
               'doctype': 'json',
               'from': 'AUTO',
               'keyfrom': 'fanyi.web',
               'salt': '16020483791551',
               'sign': '9a4be3661dede0c57a8adafae083b4f9',
               'smartresult': 'dict',
               'to': 'AUTO',
               'lts': '1602048379155',
               'version': '2.1'
               }
    r = requests.post(url, data=payload)
    trans_json = r.json()  # 返回结果定义为json
    print(trans_json)
    trans_tgt = trans_json['translateResult'][0][0]['tgt']  # 中文
    trans_src = trans_json['translateResult'][0][0]['src']  # 英文
    if str == trans_tgt:  # 如果str为中文，则返回英文，反之
        return trans_src
    else:
        return trans_tgt


if __name__ == '__main__':
    trans("good")
