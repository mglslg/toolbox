# coding=utf-8
import redis
import time
import os
import requests
import base64
import pyDes
from redis.sentinel import Sentinel

def apollo_decrypt(base64_data_str):
    k = pyDes.des(base64.b64decode('Ak9P3+MayDI='), pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None,
                  padmode=pyDes.PAD_PKCS5)
    return k.decrypt(base64.b64decode(base64_data_str))
host_list = []
if os.path.exists("./redis.txt"):
    with open('./redis.txt','r') as handler:
        redisconfig =[i.strip() for i in handler]
        port = int(redisconfig[0])
        password = redisconfig[1]
        host_list = eval(redisconfig[2])
else:
    with open('./redis.txt','w') as handler:
        req = requests.get('http://api.cfg.huli.com/configfiles/json/100000/default/techCommon.redis', verify=False).json()
        port = req['redis.saascomm.sentinel.nodes.node1.port']
        password = req['redis.saascomm.sentinel.password']
        password = password[password.find("pwd(")+4:password.rfind(')')]
        password = apollo_decrypt(password).decode('utf-8')
        for i in req.keys():
            if "host" in i and "saascomm" in i:
                sentinel_yuan = (req[i],port)
                host_list.append(sentinel_yuan)
        handler.write(port + '\n')
        handler.write(password + '\n')
        handler.write(str(host_list) + '\n')
try:
    sentinel = Sentinel(host_list)
    _redis = sentinel.master_for('mymaster', socket_timeout=0.5, password=password, db=0)
except Exception as e:
    print(e)
