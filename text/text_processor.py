import os

_data_file = os.getcwd() + '/leetcode_top.txt'


def print_user_pic():
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            row = list(line.split())
            print(row[1], row[2])


def find_intersection():
    leetcode_top = find_question('leetcode_top.txt')
    leetcode_200 = find_question('leetcode_200.txt')
    leetcode_hot100 = find_question('leetcode_hot100.txt')
    tencent_50 = find_question('tencent_50.txt')

    frequency_dict = {}
    union = set(leetcode_top) | set(leetcode_200) | set(leetcode_hot100) | set(tencent_50)
    for x in union:
        frequency_dict[x] = 0

    calc_frequency(frequency_dict, leetcode_top)
    calc_frequency(frequency_dict, leetcode_200)
    calc_frequency(frequency_dict, leetcode_hot100)
    calc_frequency(frequency_dict, tencent_50)

    time4 = []
    time3 = []
    time2 = []
    time1 = []
    for x in frequency_dict:
        if frequency_dict[x] == 4:
            time4.append(x)
        if frequency_dict[x] == 3:
            time3.append(x)
        if frequency_dict[x] == 2:
            time2.append(x)
        if frequency_dict[x] == 1:
            time1.append(x)
    print('出现4次:', time4)
    print('出现3次:', time3)
    print('出现2次:', time2)
    print('出现1次:', time1)


def calc_frequency(frequency_dict, questions):
    for x in questions:
        frequency_dict[x] = frequency_dict[x] + 1


def find_question(file_name):
    questions = []
    with open(os.getcwd() + '/' + file_name, 'rt', encoding='utf-8') as f:
        for line in f:
            row = list(line.split())
            if len(row) == 1:
                questions.append(row[0])
    return questions


if __name__ == '__main__':
    find_intersection()
