import re


def format_args(args):
    main_param = ''  # 参数
    unix98_param = {}  # -参数
    gnu_param = {}  # --参数
    if len(args) == 0:
        print('empty param !')
        return
    first_param = args[0]
    if param_style(first_param) == 'normal':
        # 有主参数,从主参数的下一个参数开始配对
        main_param = first_param
        set_param_mapping(args, 1, unix98_param, gnu_param)
    else:
        # 没有主参数,直接进行参数配对
        set_param_mapping(args, 0, unix98_param, gnu_param)

    # 参数, -参数, --参数
    return main_param, unix98_param, gnu_param


# 将参数整理为('--edit','some word')的形式
def set_param_mapping(args, start_idx, unix98_param, gnu_param):
    for i in range(start_idx, len(args)):
        if param_style(args[i]) == '-':
            if i + 1 < len(args) and param_style(args[i + 1]) == 'normal':
                unix98_param[args[i]] = args[i + 1]
            else:
                unix98_param[args[i]] = None
        elif param_style(args[i]) == '--':
            if i + 1 < len(args) and param_style(args[i + 1]) == 'normal':
                gnu_param[args[i]] = args[i + 1]
            else:
                gnu_param[args[i]] = None
        else:
            # 如果没有横杠参数就继续循环,因此就算连着出现多个normal参数也没关系,只有第一个是生效的
            continue


def param_style(param):
    if '--' in param and re.search('[A-Za-z0-9]+', param):
        return '--'
    elif '-' in param and re.search('[A-Za-z0-9]+', param):
        return '-'
    else:
        return 'normal'


def run(cmd_fn, prompt='>>>'):
    if not cmd_fn:
        print('cmd_fn can not be empty!')
        return

    while True:
        user_input = input(prompt)

        # todo 这里不能简单的split,需要做改造能够读出单引号或双引号中的内容才行
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


if __name__ == '__main__':
    rs = format_args(['-taste', '--abc', 'sdfsf', 'a', '-d', 'lalala', '-c'])
    print(rs[0])
    print(rs[1])
    print(rs[2])
