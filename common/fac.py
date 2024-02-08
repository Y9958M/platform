# -*- coding:utf-8 -*-
import time

from .cmm import threadLogs,MESSAGE, PROJECT,CLIENT,VER
from .foo import commonQueryMain,commonUpdateMain,commonRedisMain,authLoginMain, authUserButtonMain, authMenuListMain,postJobMain

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

    message.update(commonQueryMain(args_dict))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update(args_dict)
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),"client":CLIENT,"ver":VER
            ,"ldt":240202,"author":"姚鸣"})

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
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),"client":CLIENT,"ver":VER
            ,"ldt":240202,"author":"姚鸣"})
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

    message.update(commonRedisMain(args_dict))
    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),"client":CLIENT,"ver":VER
            ,"ldt":240202,"author":"姚鸣"})
    rs_name = args_dict['rs_name'] if 'rs_name' in args_dict else 'rs_name'
    userid = args_dict['userid'] if 'userid' in args_dict else 58
    logs = threadLogs(thread_id= userid,thread_name= rs_name,fac = "commonRedis",args_dict = message)
    logs.start()
    return message


# 检查登陆
def authLogin(userid,api_no:int):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message['Fac'] = '检查登陆 authLogin'
    # start 

    message.update(authLoginMain(userid))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),"client":CLIENT,"ver":VER
            ,"ldt":240202,"author":"姚鸣"})
    logs = threadLogs(thread_id = api_no ,thread_name = userid,fac = "authLogin",args_dict = message)
    logs.start()
    return message


# 员工菜单信息
def authMenuList(userid:int):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message['Fac'] = '员工菜单信息 增加META authUserMenu'
    # start 

    message.update(authMenuListMain(userid))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),"client":CLIENT,"ver":VER
            ,"ldt":240202,"author":"姚鸣"})
    return message


# 员工按钮权限
def authUserButton(userid:int):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message['Fac'] = '员工按钮权限 authUserButton 列表返回'
    # start 

    message.update(authUserButtonMain(userid))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),"client":CLIENT,"ver":VER
            ,"ldt":240202,"author":"姚鸣"})
    return message



# 推送JOB任务
def postJob(jobid:int,userid,j_args={}):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message['Fac'] = 'postJob'
    message['jobid'] = jobid
    message.update(j_args)
    # start 

    message.update(postJobMain(jobid,j_args))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),"client":CLIENT,"ver":VER
            ,"ldt":240208,"author":"姚鸣"})
    logs = threadLogs(thread_id = jobid ,thread_name = userid,fac = message['Fac'],args_dict = message)
    logs.start()
    return message
