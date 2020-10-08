import json
import re
import translator
import data_operator


def add():
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


def add_word(word):
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


def ls():
    rs = data_operator.find_all()
    for e in rs:
        print(e)


def ls_word(word):
    rs = data_operator.find(word)
    print(rs)


def exe_cmd_2param(command, fn):
    results = re.split("\\s+", command)
    if len(results) != 3:
        print("param error")
    else:
        target_word = results[2]
        fn(target_word)


def start():
    curr_words = data_operator.find_all()
    for x in curr_words:
        print(x['content'])
        for i in range(0, 3):
            input_word = input('第' + str(i) + '次:')
            if x['key'] == input_word:
                continue
            else:
                i = 0
                print('lalalalala', i)
                continue


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
            if ls_w_match:
                exe_cmd_2param(cmd, ls_word)
            elif add_w_match:
                exe_cmd_2param(cmd, add_word)
            else:
                print("command not found: " + cmd)
