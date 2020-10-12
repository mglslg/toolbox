import re
import os
import translator
import data_operator


def add_from_input():
    while True:
        en = input("请输入英文:")
        if en == 'EOF':
            break

        if data_operator.exists(en):
            print("当前单词已存在")
            continue

        cn = translator.translate(en)
        if len(cn) == 0:
            print("单词拼写错误")
            continue

        print(cn)

        data = {
            'key': en,
            'content': cn,
            'tags': []
        }
        data_operator.add(data)


def add(word=None):
    if word is not None:
        if data_operator.exists(word):
            print("当前单词已存在")
            return

        cn = translator.translate(word)
        if len(cn) == 0:
            print("单词拼写错误")
            return

        print(cn)

        data = {
            'key': word,
            'content': cn,
            'tags': []
        }
        data_operator.add(data)
    else:
        add_from_input()


def ls(word=None):
    if word is None:
        rs = data_operator.find_all()
        for e in rs:
            print(e)
    else:
        rs = data_operator.find(word)
        print(rs)


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
        else:
            ls_w_match = re.search("ls -w\\s+\\w+", cmd)
            add_w_match = re.search("add -w\\s+\\w+", cmd)
            start_n_match = re.search("start -n\\s+\\d+", cmd)
            if ls_w_match:
                exe_cmd_2param(cmd, ls)
            elif add_w_match:
                exe_cmd_2param(cmd, add)
            elif start_n_match:
                exe_cmd_2param(cmd, start)
            else:
                print("command not found: " + cmd)
