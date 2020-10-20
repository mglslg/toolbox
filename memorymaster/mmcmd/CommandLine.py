import re


def exe_cmd_2param(command, fn):
    results = re.split("\\s+", command)
    if len(results) != 3:
        print("param error")
    else:
        target_word = results[2]
        fn(target_word)


class CommandLine:
    def __init__(self, cmd, cmd_configs):
        self.__cmd = cmd
        self.__cmd_configs = cmd_configs

    def exec(self):
        print(self.__cmd)


class CommandConfig:
    # 如果有多个参数，那么第一个参数判断调用的fn，其余参数均传给fn
    def __init__(self, cmd_key, cmd_param, fn):
        self.cmd_key = cmd_key
        self.cmd_param = cmd_param
        self.fn = fn
