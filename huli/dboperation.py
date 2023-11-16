from pymongo import MongoClient
#from sshtunnel import SSHTunnelForwarder
import pymysql
#import pdb


#添加进件到mongo
def add_loan_to_mongo(loan_id,require_code,borrow_name,fund_product):
    #client = MongoClient('mongodb://saas_dev_admin:Saas_dev@192.168.102.31:27017')
    client = MongoClient('192.168.102.31',27017)
    mydb = client['saas_harbour']
    mydb.authenticate('saas_dev_admin', 'Saas_dev')

    db_loanInfo = mydb["loanInfo"]

    #result = db_loanInfo.find({"loanId":"202003261048260001"})
    db_loanInfo.insert_one({"loanId":loan_id,"requireCode":require_code,"borrowName":borrow_name,"fundProduct":fund_product})

    '''
    print('.......Start')
    for x in result:
        print('loanId is: '+x['loanId'])
    print('.......End')
    '''


#添加进件到mysql
def add_loan_to_mysql(idStart,number):
    db_saas={
        "host":"192.168.101.47",
        "user":"saas_dev_admin",
        "password":"Saas_dev",
        "db":"saas_fund_harbour",
        "charset":"utf8",
        "ssl":{"ssl":{}}  #很屎虽然什么都没填但是必须有这项配置
    }
    db_local={
        "host":"localhost",
        "user":"slg",
        "password":"enter",
        "db":"huli_demo",
        "charset":"utf8"
    }

    #saas_db = pymysql.connect(host='192.168.101.47',port = 3306,user='saas_dev_admin',passwd='Saas_dev',db ='saas_fund_harbour')
    db = pymysql.connect(**db_saas)
    cursor=db.cursor()

    #cursor.execute("select * from fund_loan where loan_id='202003261048260001'")
    loan_id_num=int(idStart)

    for i in range(number):
        loan_id = str(loan_id_num)
        insert_sql="insert into `fund_loan` ( `update_time`, `fund_code`, `user_type`, `expected_amount`, `require_code`, `partner_rate`, `apply_city_id`, `approve_repay_method`, `approve_periods`, `broker_account`, `update_user`, `approve_periods_unit`, `fund_id`, `loan_amount`, `abandon_reason`, `approve_amount`, `broker_account_name`, `repay_method`, `create_time`, `server_rate`, `org_rebate_rate`, `borrow_name`, `repay_method_name`, `fund_type`, `approve_remark`, `org_rebate_fre`, `loan_id`, `approve_status`, `apply_id`, `expected_periods`, `borrow_mobile`, `apply_city_name`, `expected_periods_unit`, `borrow_id5`, `fund_name`, `client_id`, `fund_product_name`, `partner_channel_code`, `approve_time`, `fund_product`, `loan_time`, `create_user`, `root_require_code`, `approve_repay_method_name`, `apply_time`, `partner_pay_type`) values ( now(), '', '2', '4300000', '1204213923985756164', '11', '120000', '2', '6', '666', 'wangzc', '1', '24', '0', null, '1000', '', '1', now(), '11', '2', '张三', '等额本息', null, '', '1', "+loan_id+", '12', '4', '12', '15512345678', '天津', '1', '', '浦发天津', '3b7c4285fd8861131ed7a246afb4816b', '浦发房贷', '', now(), '4', null, 'admin', null, '', '2020-01-13 00:00:00', '1')"

        try:
            print("正在创建第"+str(i)+"条记录...")
            cursor.execute(insert_sql)
            db.commit()
            add_loan_to_mongo(loan_id,"1204213923985756164","张三","浦发房贷")
        except Exception as e:
            traceback.print_exc()
            print("Error: unable to insert data")
            db.rollback()

        loan_id_num=loan_id_num+1

    db.close()


if __name__ == '__main__':
    add_loan_to_mysql(config['id_start'],config['number'])
    add_task(config['taskName'],config['execKey'],config['execName'],config['id_start'])

