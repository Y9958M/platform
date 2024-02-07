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

    VER = 240201
    PROJECT = "YM"
    ADMIN = [18550994992]
    CLIENT ="Dev:10.56"
    MESSAGE = {
        "code": 500,
        "sid":  SID,
        "count":  0,
        "msg":  '',
        "project":PROJECT,
        "client":CLIENT
    }
    DB_LINK = {
        'YM':{
            "USE" : {},
            "TYPE": "MYSQL",
            "HOST": "localhost",
            "PORT": 3306,
            "USER": "root",
            "PWD": "shtm2023",
        },
        'REDIS': {
            "DB": SID,
            "HOST": "localhost",
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
            'HOST':'localhost',
            'PORT':3310,
            'DB'  :'plm',
            'USER':'root',
            'PWD' :'4197'
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





