import re
import os
import translator
import data_operator
import datetime
from mmdb import EnDict


def add_from_input():
    while True:
        en = input("请输入英文:")
        if en == '/quit':
            break

        if data_operator.exists(en):
            print("当前单词已存在")
            continue

        cn = translator.translate(en)
        if len(cn) == 0:
            print("单词拼写错误")
            continue

        word = EnDict.get_or_none(key=en)

        if word is None:
            print(cn)
            dao = EnDict.create(key=en, content=cn, create_time=datetime.datetime.now())
            dao.save()
        else:
            print("当前单词已存在")


def add(word=None):
    if word is not None:
        if EnDict.get_or_none(key=word) is not None:
            print("当前单词已存在")
            return

        cn = translator.translate(word)
        if len(cn) == 0:
            print("单词拼写错误")
            return

        print(cn)

        dao = EnDict.create(key=word, content=cn, create_time=datetime.datetime.now())
        dao.save()
    else:
        add_from_input()


def ls(word=None):
    if word is None:
        rs = EnDict.select(EnDict.key, EnDict.content)
        for e in rs:
            print(e.key, e.content)
    else:
        rs = EnDict.select().where(EnDict.key == word)
        for e in rs:
            print(e.key, e.content)


def delete(key):
    data_operator.delete(key)


def start(num_str='3'):
    curr_words = data_operator.find_all()
    for x in curr_words:
        i = 1
        n = int(num_str)
        while i <= n:
            print(x['content'])
            input_word = input('还需输入' + str(n - i + 1) + '次:')
            if x['key'] == input_word:
                # TERM=xterm-color
                os.system('clear')
                i = i + 1
                continue
            else:
                print('单词拼写错误,大侠请重新来过!')
                i = 1
                continue
    print('战斗胜利!')


def exe_cmd_2param(command, fn):
    results = re.split("\\s+", command)
    if len(results) != 3:
        print("param error")
    else:
        target_word = results[2]
        fn(target_word)


if __name__ == '__main__':
    while True:
        cmd = input(">>> ")
        if cmd == 'exit':
            break
        if cmd == 'add':
            add()
        elif cmd == 'ls':
            ls()
        elif cmd == 'start':
            start()
        elif cmd == 'grep':
            rs = os.system('grep look words_data.txt')
            print(rs)
        else:
            ls_w_match = re.search("ls -w\\s+\\w+", cmd)
            add_w_match = re.search("add -w\\s+\\w+", cmd)
            del_w_match = re.search("delete -w\\s+\\w+", cmd)
            start_n_match = re.search("start -n\\s+\\d+", cmd)
            if ls_w_match:
                exe_cmd_2param(cmd, ls)
            elif add_w_match:
                exe_cmd_2param(cmd, add)
            elif del_w_match:
                exe_cmd_2param(cmd, delete)
            elif start_n_match:
                exe_cmd_2param(cmd, start)
            else:
                print("command not found: " + cmd)
