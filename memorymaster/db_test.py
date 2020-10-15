import mmdb
import datetime

if __name__ == '__main__':
    key = mmdb.EnDict.get_or_none(key="abc")
    if key is None:
        en_dict = mmdb.EnDict.create(key="abc", content="lalala", create_time=datetime.datetime.now())
        en_dict.save()
    else:
        print("重复了")

