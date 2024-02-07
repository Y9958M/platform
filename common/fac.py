# -*- coding:utf-8 -*-
import time

from main import threadLogs,MESSAGE, PROJECT,CLIENT,VER
from .foo import commonQueryMain,commonUpdateMain,commonRedisMain

# author  :don
# date    :20240202
# description: 接待入口 包装层面 不处理入参检查 通用 JOB功能 项目区分

# 通用【查询】对外服务 
def commonQuery(args_dict):
    message = MESSAGE.copy()
    message['Fac'] = '通用查询'
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # start 
    AUTHOR = "姚鸣"
    LDT = 240202
    # start

    message.update(commonQueryMain(args_dict))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update(args_dict)
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),
            "client":CLIENT,"author":AUTHOR,"ldt":LDT,"ver":VER})

    sqlid = args_dict['sqlid'] if 'sqlid' in args_dict else 'NULL'
    userid = args_dict['userid'] if 'userid' in args_dict else 58
    logs = threadLogs(thread_id= userid,thread_name= sqlid,fac= "commonQuery",args_dict= message)
    logs.start()
    return message



# 通用【更新】 0更新 返回COUNT
def commonUpdate(args_dict):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message.update(args_dict)
    message['Fac'] = '通用更新'
    # start
    AUTHOR = "姚鸣"
    LDT = 240202
    # 221220 语句FUN更新
    message.update(commonUpdateMain(args_dict))
    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),
            "client":CLIENT,"author":AUTHOR,"ldt":LDT,"ver":VER})
    sqlid = args_dict['sqlid'] if 'sqlid' in args_dict else 'NULL'
    userid = args_dict['userid'] if 'userid' in args_dict else 58
    logs = threadLogs(thread_id= userid,thread_name= sqlid,fac= "commonUpdate",args_dict= message)
    logs.start()
    return message



# 通用【缓存】
def commonRedis(args_dict):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message.update(args_dict)
    message['Fac'] = '通用缓存 入参 redis_type redis_db rs_name rs_key rs_val proj_name sqlid time_expire'
    # start
    AUTHOR = "姚鸣"
    LDT = 240202

    message.update(commonRedisMain(args_dict))
    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),
            "client":CLIENT,"author":AUTHOR,"ldt":LDT,"ver":VER})
    rs_name = args_dict['rs_name'] if 'rs_name' in args_dict else 'rs_name'
    userid = args_dict['userid'] if 'userid' in args_dict else 58
    logs = threadLogs(thread_id= userid,thread_name= rs_name,fac = "commonRedis",args_dict = message)
    logs.start()
    return message


# 通用【推送】  TODO


