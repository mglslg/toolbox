import re
import os
import translator
import datetime
from mmdb import EnDict
import json
from prettytable import PrettyTable


def add_from_input():
    while True:
        en = input("请输入英文:").strip()
        if en == '/q' or en == '/quit':
            break

        if EnDict.get_or_none(key=en) is not None:
            print("当前单词已存在")
            continue

        rs = translator.translate(en)
        cn = rs[0]
        voice = rs[1]
        example = rs[2]
        if len(cn) == 0:
            print("单词拼写错误")
            continue

        word = EnDict.get_or_none(key=en)

        if word is None:
            print(cn)
            print(voice)
            print(example)
            dao = EnDict.create(key=en, content=cn, create_time=datetime.datetime.now(),
                                show_time=datetime.datetime.now(), voice=voice, example=example)
            dao.save()
        else:
            print("当前单词已存在")


def add(word=None):
    if word is not None:
        word = word.strip()
        if EnDict.get_or_none(key=word) is not None:
            print("当前单词已存在")
            return

        rs = translator.translate(word)
        cn = rs[0]
        voice = rs[1]
        example = rs[2]
        if len(cn) == 0:
            print("单词拼写错误")
            return

        print(cn)
        print(voice)
        print(example)

        now = datetime.datetime.now()
        dao = EnDict.create(key=word, content=cn, create_time=now, show_time=now, voice=voice, example=example)
        dao.save()
    else:
        add_from_input()


def ls(word=None):
    if word is None:
        rs = EnDict.select()
        for e in rs:
            print(e.key, e.content, e.voice)
    else:
        rs = EnDict.select().where(EnDict.key == word)
        for e in rs:
            print(e.key, e.content, e.voice)


def delete(key):
    EnDict.delete().where(EnDict.key == key).execute()


def refresh(key=None):
    if key is None:
        rs = EnDict.select()
        for x in rs:
            curr_word = x.key
            tran = translator.translate(curr_word)
            new = {'content': tran[0],
                   'voice': tran[1],
                   'example': tran[2]
                   }
            EnDict.update(new).where(EnDict.key == curr_word).execute()
            print("更新", curr_word)
    else:
        curr_data = EnDict.get_or_none(key=key)
        if curr_data is None:
            print("不存在当前单词")
        else:
            tran = translator.translate(key)
            new = {'content': tran[0],
                   'voice': tran[1],
                   'example': tran[2]
                   }
            EnDict.update(new).where(EnDict.key == key).execute()


def start(num_str='10'):
    # 注意这里peewee的逻辑操作符只有【& | == ~ 】,什么is not之类都不能用！
    curr_words = EnDict.select().where((EnDict.is_open == True) & (EnDict.show_time < datetime.datetime.now()))

    for x in curr_words:
        i = 1
        n = int(num_str)
        while i <= n:
            t = PrettyTable(["单词", "例句"])
            t.add_row(['\n'+x.content, get_exp(i, x.key, x.example)])
            print(t)

            input_word = input('还需输入' + str(n - i + 1) + '次:').strip()
            if input_word == 'fuck':
                os.system('clear')
                pt = PrettyTable(["单词", "音标"])
                pt.add_row([x.key, x.voice])
                print(pt)
                i = 1
                continue
            if input_word == '/voice':
                os.system('clear')
                pt = PrettyTable(["音标"])
                pt.add_row([x.voice])
                print(pt)
                i = 1
                continue
            if input_word == '/q' or input_word == '/quit':
                return
            if x.key == input_word:
                # TERM=xterm-color
                os.system('clear')
                i = i + 1
                if i == n:
                    do_pass(x)
                continue
            else:
                print('单词拼写错误,大侠请重新来过!\n\n')
                i = 1
                continue
    print('战斗胜利!')


def get_exp(count, word, examples):
    exp_array = json.loads(examples)
    length = len(exp_array)
    if length > 0:
        return str(exp_array[count % length]).replace(word, "(?)")


def do_pass(old):
    now = datetime.datetime.now()
    old_count = int(old.pass_count)
    is_open = True
    show_time = old.show_time

    if old_count == 0:
        show_time = now + datetime.timedelta(days=1)
    elif old_count == 1:
        show_time = now + datetime.timedelta(days=1)
    elif old_count == 2:
        show_time = now + datetime.timedelta(days=3)
    elif old_count == 3:
        show_time = now + datetime.timedelta(days=5)
    elif old_count == 4:
        show_time = now + datetime.timedelta(days=10)
    elif old_count == 5:
        show_time = now + datetime.timedelta(days=30)
    else:
        is_open = False

    new = {'is_open': is_open,
           'pass_time': now,
           'show_time': show_time,
           'pass_count': old_count + 1
           }

    EnDict.update(new).where(EnDict.key == old.key).execute()


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
        if cmd == 'quit':
            break
        if cmd == 'add':
            add()
        elif cmd == 'ls':
            ls()
        elif cmd == 'start':
            start()
        elif cmd == 'refresh':
            refresh()
        else:
            ls_w_match = re.search("ls -w\\s+\\w+", cmd)
            add_w_match = re.search("add -w\\s+\\w+", cmd)
            del_w_match = re.search("delete -w\\s+\\w+", cmd)
            start_n_match = re.search("start -n\\s+\\d+", cmd)
            refresh_w_match = re.search("refresh -w\\s+\\w+", cmd)
            # help 待实现
            if ls_w_match:
                exe_cmd_2param(cmd, ls)
            elif add_w_match:
                exe_cmd_2param(cmd, add)
            elif del_w_match:
                exe_cmd_2param(cmd, delete)
            elif start_n_match:
                exe_cmd_2param(cmd, start)
            elif refresh_w_match:
                exe_cmd_2param(cmd, refresh)
            else:
                print("command not found: " + cmd)
