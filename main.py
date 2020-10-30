import sys

# print("当前的工作目录：", os.getcwd())
sys.path.append("/Users/suolongga/PycharmProjects/toolbox/memorymaster")
sys.path.append("/Users/slg/PyProj/toolbox/memorymaster")
# print("python搜索模块的路径集合", sys.path)

from cltable import *
from memorymaster import *
from translate import *

if __name__ == '__main__':
    while True:
        print("欢迎来到嘎子的工具箱")
        print('1. 标题生成器')
        print('2. 记忆大师')
        print('3. 中英翻译')
        select_menu = input("请选择菜单:")
        if select_menu == 'quit' or select_menu == 'exit':
            break
        if select_menu == '1':
            title = input("请输入标题:")
            dividing_line.print_title(title)
        elif select_menu == '2':
            words.main()
        elif select_menu == '3':
            translator.main()
        else:
            print('请选择正确的菜单!')
