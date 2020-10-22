import re


def format_args(args):
    unix98_options = []
    gnu_options = []
    param_list = []
    for x in args:
        if '--' in x and re.search('[A-Za-z0-9]+', x):
            gnu_options.append(x)
        elif '-' in x and re.search('[A-Za-z0-9]+', x):
            unix98_options.append(x)
        else:
            param_list.append(x)
    u98 = unix98_options
    gnu = gnu_options
    arg = param_list
    if len(unix98_options) == 1:
        u98 = unix98_options[0]
    if len(gnu_options) == 1:
        gnu = gnu_options[0]
    if len(param_list) == 1:
        arg = param_list[0]
    return u98, gnu, arg


def run(cmd_fn, prompt='>>>'):
    if not cmd_fn:
        print('cmd_fn can not be empty!')
        return

    while True:
        user_input = input(prompt)
        args = user_input.split()

        if not args:
            continue

        cmd_key = args[0]

        if user_input == 'quit' or user_input == 'exit':
            break
        elif cmd_key in cmd_fn:
            f = cmd_fn[cmd_key]
            if len(args) == 1:
                f()
            else:
                f(args[1:])
        else:
            print('command not found: ' + user_input)


def test1():
    print('test1')


def test2(param1, param2, param3):
    print('test2')


if __name__ == '__main__':
    print(len('abc'))
    rs = format_args(['-w', '--abc', '--5', 'a', 'sdf', '-', '--'])
    rs = format_args(['-w', '--abc', '--5', 'a'])
    print(rs[0])
    print(rs[1])
    print(rs[2])

if __name__ == '__main__1':
    while True:
        print("欢迎来到嘎子的工具箱")
        print('1. lalalala')
        print('2. heiheiheihei')
        select_menu = input("请选择菜单:")
        if select_menu == '1':
            cmd_mapping = {
                'test': test1
            }
            run(cmd_mapping)
        else:
            cmd_mapping = {
                'test': test2
            }
            run(cmd_mapping)
