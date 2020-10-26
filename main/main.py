from cltable import dividing_line
from memorymaster import words

if __name__ == '__main__':
    while True:
        print("欢迎来到嘎子的工具箱")
        print('1. 标题生成器')
        print('2. 记忆大师')
        print('3. 中英翻译')
        select_menu = input("请选择菜单:")
        if select_menu == '1':
            title = input("请输入标题:")
            dividing_line.print_title(title)
        elif select_menu == '2':
            words.main()
        else:
            print('请选择正确的菜单!')
