import json
import re
import os
import translator

# print(os.path.abspath("."))
_data_file = os.getcwd() + '/words_data.txt'


def key_exists(key):
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            if key == curr_data['key']:
                return True


def add():
    while True:
        en = input("请输入英文:")
        if en == 'EOF':
            break

        if key_exists(en):
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
        with open(_data_file, 'at', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')


def add_word(word):
    if key_exists(word):
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
    with open(_data_file, 'at', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')


def ls():
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            print(curr_data)


def ls_word(word):
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            if curr_data['key'] == word:
                print(curr_data)


def exe_cmd_2param(command, fn):
    results = re.split("\\s+", command)
    if len(results) != 3:
        print("param error")
    else:
        target_word = results[2]
        fn(target_word)


def start():
    curr_words = []
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            curr_words.append(curr_data)

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
