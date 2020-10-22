import re
import os
import translator
import datetime
from mmdb import EnDict
import json
from prettytable import PrettyTable
from cmd import command_line as cl


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


def add(args=None):
    if not args:
        add_from_input()
    else:
        rs = cl.format_args(args)
        word = rs[2]
        if not word:
            print('参数格式有误')
        else:
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


def ls(args=None):
    if args is None:
        rs = EnDict.select()
        for e in rs:
            print(e.key, e.content, e.voice)
    else:
        rs = EnDict.select().where(EnDict.key == cl.format_args(args)[2])
        for e in rs:
            print(e.key, e.content, e.voice)


def remove(args=None):
    if not args:
        print('请输入要删除的单词')
    else:
        EnDict.delete().where(EnDict.key == cl.format_args(args)[2]).execute()


def refresh(args=None):
    if args is None:
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
        key = cl.format_args(args)[2]
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


def start(args=None):
    num_str = '10'
    if args:
        num_str = cl.format_args(args)[2]

    # 注意这里peewee的逻辑操作符只有【& | == ~ 】,什么is not之类都不能用！
    curr_words = EnDict.select().where((EnDict.is_open == True) & (EnDict.show_time < datetime.datetime.now()))

    for x in curr_words:
        i = 1
        n = int(num_str)
        while i <= n:
            t = PrettyTable(["单词", "例句"])
            t.add_row(['\n' + x.content, get_exp(i, x.key, x.example)])
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


if __name__ == '__main__':
    cmd_mapping = {
        'add': add,
        'ls': ls,
        'start': start,
        'refresh': refresh,
        'rm': remove
    }
    cl.run(cmd_mapping)
