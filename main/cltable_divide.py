from prettytable import PrettyTable
# from prettytable import MSWORD_FRIENDLY


def print_title(title):
    pt = PrettyTable([title])
    pt.add_row([title])
    pt.border = True
    pt.header = False
    pt.padding_width = 20
    # pt.set_style(MSWORD_FRIENDLY)
    print(pt)


if __name__ == '__main__':
    title = input("请输入标题:")
    print_title(title)
