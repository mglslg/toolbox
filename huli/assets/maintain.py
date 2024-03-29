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


# 设置任务为已办
def set_task_done():
    sql = "UPDATE `soeasy_assets_rule`.`assets_user_task_info` SET t.task_status = 3, t.decision = 'data_clean' WHERE task_id in (" + id_with_quot() + ")"
    print(sql)


if __name__ == '__main__':
    # 删除废弃档案
    # delete_warrant()

    # 修改档案保管地 西安
    update_warrant_place('610100')

    # 修改为403已出库
    # update_warrant_status('403')

    # 将废弃任务设置为已办
    # set_task_done()
