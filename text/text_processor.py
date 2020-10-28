import os

_data_file = os.getcwd() + '/temp.txt'


def print_user_pic():
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            row = list(line.split())
            if len(row) == 3:
                print('cnMap.put("' + row[1] + '","' + row[2] + '");')
            else:
                if len(row) != 0:
                    print(row)


if __name__ == '__main__':
    print_user_pic()
