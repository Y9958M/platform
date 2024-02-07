# -*- coding:utf-8 -*-
import time

from main import threadLogs,MESSAGE, PROJECT,CLIENT,VER
from .foo import authLoginMain, authUserButtonMain, authMenuListMain

# author  :don
# date    :2024-02-02
# description: 用户 组织 角色 菜单 数据 对外提供的标准服务 已组装好内部服务
# API只做认证 数据在后台 USERID 
# 去年了业务域

# 检查登陆
def authLogin(userid,api_no:int):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message['Fac'] = '检查登陆 authLogin'
    AUTHOR = "姚鸣"
    LDT = 240202
    # start 

    message.update(authLoginMain(userid))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),
        "client":CLIENT,"author":AUTHOR,"ldt":LDT,"ver":VER})
    logs = threadLogs(thread_id = api_no ,thread_name = userid,fac = "authLogin",args_dict = message)
    logs.start()
    return message


# 员工菜单信息
def authMenuList(userid:int):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message['Fac'] = '员工菜单信息 增加META authUserMenu'
    AUTHOR = "姚鸣"
    LDT = 240202
    # start 

    message.update(authMenuListMain(userid))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),
        "client":CLIENT,"author":AUTHOR,"ldt":LDT,"ver":VER})
    return message


# 员工按钮权限
def authUserButton(userid:int):
    start_time = time.time()
    start_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = MESSAGE.copy()
    message['Fac'] = '员工按钮权限 authUserButton 列表返回'
    AUTHOR = "姚鸣"
    LDT = 240202
    # start 

    message.update(authUserButtonMain(userid))

    # end
    end_strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    d_time = time.time() - start_time
    message.update({'start_time':start_strftime,'end_time':end_strftime,'times':round(d_time,2),
        "client":CLIENT,"author":AUTHOR,"ldt":LDT,"ver":VER})
    return message
