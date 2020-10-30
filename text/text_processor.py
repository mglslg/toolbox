import os

_data_file = os.getcwd() + '/temp1.txt'


def print_user_pic():
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            row = list(line.split())
            print(row[1], row[2])


if __name__ == '__main__':
    print_user_pic()
