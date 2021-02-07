def id_with_quot():
    ids = ''
    with open('warrantIds.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            ids = ids + "'" + str.strip(line) + "'" + ","
    char_array = list(ids)
    char_array.pop()
    warrant_ids = ''.join(char_array)
    return warrant_ids


def id_no_quot():
    ids = ''
    with open('warrantIds.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            ids = ids + str.strip(line) + ','
    char_array = list(ids)
    char_array.pop()
    warrant_ids = ''.join(char_array)
    return warrant_ids


# 删除档案
def delete_warrant():
    sql = "delete from `soeasy_assets_rule`.`warrant` where id in (" + id_no_quot() + ");"
    print(sql)


# 修改档案状态
def update_warrant_status(status):
    mysql = "update `soeasy_assets_rule`.`warrant` set warrant_status=" + status + " where id in (" + id_no_quot() + ");"
    mongo = "db.warrantInfo.update( {'warrantId':{$in:[" + id_with_quot() + "]}}, {$set:{'warrantStatus':'" + status + "'}}, {multi:true,upsert:false} )"
    print(mysql)
    print(mongo)


# 修改档案保管地
def update_warrant_place(code):
    mysql = "update `soeasy_assets_rule`.`warrant` set warrant_place=" + code + " where id in (" + id_no_quot() + ");"
    mongo = "db.warrantInfo.update( {'warrantId':{$in:[" + id_with_quot() + "]}}, {$set:{'warrantPlace':'" + code + "'}}, {multi:true,upsert:false} )"
    print(mysql)
    print(mongo)


if __name__ == '__main__':
    # 删除废弃档案
    #delete_warrant()

    # 修改档案保管地
    #update_warrant_place('320300')

    # 修改为403已出库
    update_warrant_status('403')


