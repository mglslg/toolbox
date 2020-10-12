import os
import json

# print(os.path.abspath("."))
_data_file = os.getcwd() + '/words_data.txt'


def add(data):
    with open(_data_file, 'at', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')


def delete(key):
    with open(_data_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(_data_file, "w", encoding="utf-8") as f_w:
        for line in lines:
            curr_data = json.loads(line)
            if curr_data['key'] == key:
                continue
            f_w.write(line)


def update(data):
    print('update')


def find(key):
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            if curr_data['key'] == key:
                return curr_data


def find_all():
    result = []
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            result.append(curr_data)
    return result


def exists(key):
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            if key == curr_data['key']:
                return True


def get_by_key(key):
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            curr_data = json.loads(line)
            if key == curr_data['key']:
                return curr_data
