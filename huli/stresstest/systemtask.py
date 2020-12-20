import requests
def add_task(taskName,execKey,execName,idStart):
    url = "http://yun.huli.com/risk-base/systemtask/saveOrUpdate"
    data = {
        "bizKey":"1",
        "conditionType":"1",
        "executeFlag":"2",
        "executeSelfdefiDay":"2020-08-03",
        "executeTime":"13:05:38",
        "judgingCondition":'[{"ref_plugin":"","plugin_start":"(","param_code":"loanId","con_plugin":">=","column_value":"'+idStart+'","plugin_end":")","isSelect":false}]',
        "systemCode":"harbour",
        "taskExecuteKey":execKey,
        "taskExecuteName":execName,
        "taskName":taskName,
        "taskType":"1"
    }
    h = {
        "User-Agent": "Android/H60-L01/8.1.0/",
        "cookie":"HttpOnly; HttpOnly; auth_info=c3VvbG9uZ2dhfDE1OTYwMTA3MzQ4MTA=; auth_hash=e8340e3e93b0f850905f6bb2400437b3; HttpOnly; JSESSIONID=9085AFF00571013B6F8064498D00396B; _saasadminsid=9f04b81d-9cb6-4af1-8d9f-02deccc7a80f",
        "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYWFzIiwiYXVkIjoicmlzay1iYXNlIiwicGFzc3dvcmQiOiI2MjdmODNlYzBlZjQyOTI5MmQyNDg2ZTZmNjA4ZTU3ZCIsImlzcyI6Imh1bGkiLCJleHAiOjE1OTkwOTg0NjQsImlhdCI6MTU5NjUwNjQ2NCwianRpIjoiNTA4YmQ2ODViNzI1NDE3OWFjYTZjNjQ0N2ViMjlhNGMiLCJ1c2VybmFtZSI6InN1b2xvbmdnYSJ9.pitMvfdUk4e7LdoaVi1JTn4hwFPxh43SFJjtr9uMpyg"
    }
    res = requests.post(url, data=data, headers=h)
    print(res.json())

