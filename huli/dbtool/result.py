import pymysql
import sys
import datetime
from testconfig import config
from testconfig import dubbo_config
from testconfig import db_config


def gen_report(id_prefix):
    db_saas = {
        "host": "192.168.101.47",
        "user": "saas_dev_admin",
        "password": "Saas_dev",
        "db": "saas_fund_harbour",
        "charset": "utf8",
        "ssl": {"ssl": {}}  # 很屎虽然什么都没填但是必须有这项配置
    }

    db = pymysql.connect(**db_saas)
    cursor = db.cursor()

    startTimeSql = "select start_time from process_monitor where (business_key like '" + id_prefix + "%') order by start_time asc limit 1"

    endTimeSql = "select start_time from process_monitor where (business_key like '" + id_prefix + "%' ) order by start_time desc limit 1"

    correctNumSql = "select count(*) from process_monitor where business_key LIKE '" + id_prefix + "%' and inst_status=2"
    # correctNumSql="select count(*) from process_monitor where business_key LIKE '"+id_prefix+"%'"

    print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<< " + config['taskName'] + " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    print("ID起始:%s " % config['id_start'])
    print("ID前缀:%s " % config['id_prefix'])
    print("执行流程:%s " % config['execName'])
    print("流程key:%s " % config['execKey'])

    cursor.execute(startTimeSql)
    starttime = cursor.fetchone()
    print("开始时间: %s " % starttime)

    cursor.execute(endTimeSql)
    endtime = cursor.fetchone()
    print("结束时间: %s " % endtime)

    print("执行总数: %s " % config['number'])

    cursor.execute(correctNumSql)
    correctNum = cursor.fetchone()
    print("成功个数: %s " % correctNum)

    print("\ndubbo配置:")
    for k in dubbo_config.keys():
        print(k, ":", dubbo_config[k])

    print("\n数据库配置:")
    for k in db_config.keys():
        print(k, ":", db_config[k])

    print("------------------------------------------------------------------------")


if __name__ == '__main__':
    gen_report(config['id_prefix'])
