import os
import translator
import datetime
from mm_db import EnDict
from mm_db import SysUser
import json
from prettytable import PrettyTable
import cmd_launcher as cl
import hashlib
import cltable_divide as cltable

_curr_user = ''


def add_from_input():
    while True:
        en = input("请输入英文:").strip()
        if en == '/q' or en == '/quit':
            break

        if EnDict.get_or_none(key=en, username=_curr_user) is not None:
            print("当前单词已存在")
            continue

        rs = translator.translate(en)
        cn = rs[0]
        voice = rs[1]
        example = rs[2]
        if len(cn) == 0:
            print("单词拼写错误")
            continue

        word = EnDict.get_or_none(key=en, username=_curr_user)

        if word is None:
            print(cn)
            print(voice)
            print(example)
            dao = EnDict.create(key=en, content=cn, create_time=datetime.datetime.now(),
                                show_time=datetime.datetime.now(), voice=voice, example=example, username=_curr_user)
            dao.save()
        else:
            print("当前单词已存在")


def add(args=None):
    if not args:
        add_from_input()
    else:
        cl_rs = cl.format_args(args)
        word = cl_rs[0]
        if not word:
            print('参数格式有误')
        elif cl_rs[1]:
            options = cl_rs[1]
            custom_eg = None
            eg_tag = None
            if '-e' in options:
                custom_eg_en = input('请输入例句:')
                custom_eg_cn = input('请输入翻译:')
                if custom_eg_en.strip() == '' and custom_eg_cn.strip() == '':
                    custom_eg = None
                else:
                    custom_eg = custom_eg_en + '\n' + custom_eg_cn
            if '-t' in options:
                eg_tag = input('请输入标签:')
                if eg_tag.strip() == '':
                    eg_tag = None
            add_word(word, custom_eg, eg_tag)
        else:
            add_word(word)


def edit(args):
    cl_rs = cl.format_args(args)
    word = cl_rs[0]
    options = cl_rs[1]
    if not word:
        print('参数格式有误,缺少单词!')
        return
    if not options:
        print('参数格式有误,缺少编辑选项!')
        return
    word_obj = EnDict.get_or_none(key=word, username=_curr_user)
    if not word_obj:
        print('单词尚不存在,请先添加!')
        return
    custom_eg = word_obj.custom_eg
    eg_tag = word_obj.eg_tag
    if '-e' in options:
        custom_eg_en = input('请输入例句:')
        custom_eg_cn = input('请输入翻译:')
        if custom_eg_en.strip() == '' and custom_eg_cn.strip() == '':
            custom_eg = None
        else:
            custom_eg = custom_eg_en + '\n' + custom_eg_cn
    if '-t' in options:
        eg_tag = input('请输入标签:')
        if eg_tag.strip() == '':
            eg_tag = None
    EnDict.update(custom_eg=custom_eg, eg_tag=eg_tag).where(
        (EnDict.key == word) & (EnDict.username == _curr_user)).execute()


def add_word(word, custom_eg=None, eg_tag=None):
    word = word.strip()
    if EnDict.get_or_none(key=word, username=_curr_user) is not None:
        print("当前单词已存在")
        return

    rs = translator.translate(word)
    if rs:
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
        dao = EnDict.create(key=word, content=cn, create_time=now, show_time=now, voice=voice, example=example,
                            custom_eg=custom_eg, eg_tag=eg_tag, username=_curr_user)
        dao.save()


def ls(args=None):
    if args is None:
        rs = EnDict.select().where(EnDict.username == _curr_user)
        for e in rs:
            print(e.key, e.content, e.voice)
    else:
        rs = EnDict.select().where((EnDict.key == cl.format_args(args)[0]) & (EnDict.username == _curr_user))
        for e in rs:
            print(e.key, e.content, e.voice, '\n')
            exp_array = json.loads(e.example)
            for x in exp_array:
                print(str(x)[2:])
            if e.custom_eg:
                print(e.custom_eg, "————《" + e.eg_tag + "》\n")


def remove(args=None):
    if not args:
        print('请输入要删除的单词')
    else:
        EnDict.delete().where((EnDict.key == cl.format_args(args)[0]) & (EnDict.username == _curr_user)).execute()


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
            EnDict.update(new).where((EnDict.key == curr_word) & (EnDict.username == _curr_user)).execute()
            print("更新", curr_word)
    else:
        key = cl.format_args(args)[0]
        curr_data = EnDict.get_or_none(key=key, username=_curr_user)
        if curr_data is None:
            print("不存在当前单词")
        else:
            tran = translator.translate(key)
            new = {'content': tran[0],
                   'voice': tran[1],
                   'example': tran[2]
                   }
            EnDict.update(new).where((EnDict.key == key) & (EnDict.username == _curr_user)).execute()


def start(args=None):
    num_str = '6'
    if args:
        num_str = cl.format_args(args)[0]

    # 注意这里peewee的逻辑操作符只有【& | == ~ 】,什么is not之类都不能用！
    curr_words = EnDict.select().where(
        (EnDict.is_open == True) & (EnDict.username == _curr_user) & (
                EnDict.show_time < datetime.datetime.now())).order_by(EnDict.show_time.asc())

    for x in curr_words:
        i = 1
        n = int(num_str)
        can_pass = True
        while i <= n:
            t1 = PrettyTable(["单词"])
            t1.add_row([str([x.content]).replace(x.key.title(), "???")])
            print(t1)
            print(get_exp(i, x.key, x.example))
            if x.custom_eg:
                print(x.custom_eg.replace(x.key, "(?)"), "————《" + x.eg_tag + "》\n")

            input_word = input('还需输入' + str(n - i + 1) + '次:').strip()
            if input_word == 'fuck' or input_word == '?':
                os.system('clear')
                pt = PrettyTable(["单词", "音标"])
                pt.add_row([x.key, x.voice])
                print(pt)
                i = 1
                can_pass = False
                continue
            if input_word == '/voice':
                os.system('clear')
                pt = PrettyTable(["音标"])
                pt.add_row([x.voice])
                print(pt)
                i = 1
                continue
            if input_word == '/pass':
                os.system('clear')
                do_pass(x, can_pass)
                break
            if input_word == '/q' or input_word == '/quit':
                return
            if x.key == input_word:
                # TERM=xterm-colorq
                os.system('clear')
                i = i + 1
                if i == n:
                    do_pass(x, can_pass)
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
        mask = str(exp_array[count % length]).replace(word, "(?)")[2:]
        if mask.find("(?)") == -1:
            most_like = find_most_like(mask, word)
            return mask.replace(most_like, "(?)")
        return mask


def find_most_like(sentence, target):
    max_length = 0
    most_like = ''
    word_array = sentence.split()
    for word in word_array:
        length = 0
        for i, v in enumerate(word):
            if i < len(target) and target[i].lower() == word[i].lower():
                length = length + 1
        if length > max_length:
            max_length = length
            most_like = word
    return most_like


def translate_word(word):
    __rs = translator.trans_to_format(word)
    if not __rs:
        print('查无此词!')
    else:
        print(__rs[0])
        print(__rs[1])
        answer = input('是否添加当前单词?(y/n)')
        if answer == 'y':
            add(word)
        else:
            return


def do_pass(old, can_pass):
    if not can_pass:
        return
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
        show_time = now + datetime.timedelta(days=15)
    elif old_count == 6:
        show_time = now + datetime.timedelta(days=30)
    else:
        is_open = False

    new = {'is_open': is_open,
           'pass_time': now,
           'show_time': show_time,
           'pass_count': old_count + 1
           }

    EnDict.update(new).where((EnDict.key == old.key) & (EnDict.username == _curr_user)).execute()


def main():
    username = input("请输入用户名:")
    password = input("请输入密码:")
    if SysUser.get_or_none(username=username) is None:
        cltable.print_title("当前用户不存在!")
        return
    else:
        pwd = SysUser.get_or_none(username=username).password
        if hashlib.md5(password.encode(encoding='UTF-8')).hexdigest() != pwd:
            cltable.print_title("用户名密码不正确!")
            return

    global _curr_user
    _curr_user = username

    cmd_mapping = {
        'add': add,
        'edit': edit,
        'ls': ls,
        'start': start,
        'refresh': refresh,
        'rm': remove,
        '?': translate_word
    }
    cl.run(cmd_mapping)


if __name__ == '__main__':
    print('lalala')
    # user = SysUser.select()

    # print(user)
    # pwd = hashlib.md5(b'111111').hexdigest()
    # print(pwd)
    # word = find_most_like('I have a dream', 'ha')
    # print(word)
