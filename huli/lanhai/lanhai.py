import os
import re

_data_file = os.getcwd() + '/lanhai/lanhai_db.txt'
_data_file_msg = os.getcwd() + '/lanhai/lanhai_msg.txt'


def change_txt(newId):
    after_set = ''
    after_in = ''
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            if re.search(r"in:", line):
                after_in = re.search(r"'(\d+)'", line).groups()[0]
            if re.search(r"set:", line):
                after_set = re.search(r"'(\d+)'", line).groups()[0]

    print('after_set is:', after_set)
    print('after_in is:', after_in)

    buffer = []
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            buffer.append(line.replace(after_set, newId).replace(after_in, after_set))
    with open(_data_file, 'w', encoding='utf-8') as f:
        for x in buffer:
            f.write(x)

    msg_buffer = []
    with open(_data_file_msg, 'rt', encoding='utf-8') as f:
        for line in f:
            msg_buffer.append(line.replace(after_set, newId))
    with open(_data_file_msg, 'w', encoding='utf-8') as f:
        for x in msg_buffer:
            f.write(x)


if __name__ == '__main__':
    change_txt("202012081701570002")
