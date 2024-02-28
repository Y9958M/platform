# -*- coding:utf-8 -*-
# author  :don
# date    :2024-02-01
# desc  : 仅仅提供通用服务 用户权限 全局提供基础连接 
# 设计理念
# 这不是一款SAAS化产品 而是共用一个云平台 通用查询 其它定制服务 跑在数仓DH服务器上的

# SID 环境标识 1生产 2测试 3删除 4作废 5本机开发 API 1 CMM 3 
SID = 5


# 5本机
if SID == 5:
    ADMIN = [18550994992]
    DB_LINK = {
        'YM':{
            "USE" : {},
            "TYPE": "MYSQL",
            "HOST": "127.0.0.1",
            "PORT": 3306,
            "USER": "root",
            "PWD": "shtm2023",
        },
        'REDIS': {
            "DB": SID,
            "HOST": "127.0.0.1",
            "PWD": "",
            "PORT": 6378,
            "TYPE": "REDIS"
        },
        'DH':{
            'TYPE':'MYSQL',
            'HOST':'192.168.10.222',
            'PORT':3306,
            'DB'  :'dws',
            'USER':'query',
            'PWD' :'query'
        },
        'PLM':{
            'TYPE':'MYSQL',
            'HOST':'127.0.0.1',
            'PORT':3310,
            'DB'  :'plm',
            'USER':'root',
            'PWD' :'4197'
        },
        'GRASP':{
            'TYPE':'MYSQL',
            'HOST':'127.0.0.1',
            'PORT':3310,
            'DB'  :'grasp',
            'USER':'root',
            'PWD' :'4197'
        },
    }
    PF_LINK = {
        'DH':{
            "HOST":"192.168.10.222",
            "PORT":9527,
            "USER":"admin",
            "PWD" :"123456"
        }
    }

# 2测试 expire
elif SID == 2:
    pass
#   1生产
elif SID == 1:
    pass
else:
    pass





