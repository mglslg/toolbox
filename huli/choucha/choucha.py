
_data_file = '2020092815474800001.txt'


def generate_sql():
    with open(_data_file, 'rt', encoding='utf-8') as f:
        for line in f:
            rs = line.split("|")
            if len(rs)!=5:
                print("分割异常!",rs)
                return
            task_name = rs[0].strip()
            desc = '' if rs[2].strip()=='-1' else rs[2].strip()
            time = rs[3].strip().replace("-","/")
            assignee = rs[4].strip()
            sql = "update `soeasy_risk_rule`.`user_task_info_temp` " \
                  "set outer_decision_desc ='"+desc+"' " \
                  "where  task_name='"+task_name+"' " \
                  "and complete_time='"+time+"' " \
                  "and assignee='"+assignee+"' and loan_id= "+_data_file.split(".")[0]+";"

            if desc!='1' and desc!='通过' and desc!='':
                print(sql)



if __name__ == '__main__':
    generate_sql()
