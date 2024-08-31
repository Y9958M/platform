# -*- coding:utf-8 -*-
from .cmm import threadLogs,msgWrapper
from .foo import (commonQueryMain,commonRedisMain,cmmBillidMain,cmmBillInfoMain,cmmBillDelMain
                  ,authLoginMain,ddLoginMain, authUserButtonMain, authMenuListMain,postJobMain
                  ,ddGetPermissionBraidMain)

# author  :don
# date    :20240202
# description: 接待入口 包装层面 不处理入参检查 通用 JOB功能 项目区分


@msgWrapper(ldt=20240615,s_func_remark='通用【查询】对外服务')
def commonQuery(j_args):
    j_res = commonQueryMain(j_args)
    logs = threadLogs(from_code='commonQuery', key_code= j_args.get('sqlid',''),args_in= j_args,args_out= j_res)
    logs.start()
    j_res['params'] = j_args
    return j_res


@msgWrapper(ldt=20240615,s_func_remark='通用【缓存】入参 redis_type redis_db rs_name rs_key rs_val proj_name sqlid time_expire')
def commonRedis(j_args):
    j_res = commonRedisMain(j_args)
    logs = threadLogs(from_code='commonQuery', key_code= j_args.get('sqlid',''),args_in= j_args,args_out= j_res)
    logs.start()
    j_res['params'] = j_args
    return j_res


@msgWrapper(ldt=20240228,s_func_remark='通用【单号】')
def commonBillid(s_bill_key:str,bltid=1):
    j_res = cmmBillidMain(s_bill_key, bltid=1)
    j_res['params'] = {'bill_key':s_bill_key,'bltid':bltid}
    return j_res


@msgWrapper(ldt=20240304,s_func_remark='通用【单号信息】')
def commonBillInfo(s_billid:str,s_act='query'):
    if s_act == 'query':
        j_res = cmmBillInfoMain(s_billid)
    elif s_act.lower() == 'del':
        j_res = cmmBillDelMain(s_billid)
    else:
        j_res = {'msg':'未配对通用单据动作'}
    j_res.update({'billid':s_billid})
    return j_res

@msgWrapper(ldt=20240615,s_func_remark='检查登陆')
def authLogin(j_args):
    j_res = authLoginMain(j_args)
    s_user = j_args.get('phone_no',0) if j_args.get('phone_no',0) else j_args.get('user_code','-99') 
    logs = threadLogs(from_code='authLogin', key_code= s_user,args_in= j_args,args_out= j_res)
    logs.start()

    j_res['params'] = j_args
    return j_res

@msgWrapper(ldt=20240615,s_func_remark='钉钉登陆')
def ddLogin(j_args):
    j_res = ddLoginMain(j_args)
    s_user = j_args.get('phone_no',0) if j_args.get('phone_no',0) else j_args.get('user_code','-99') 
    logs = threadLogs(from_code='authLogin', key_code= s_user,args_in= j_args,args_out= j_res)
    logs.start()

    j_res['params'] = j_args
    return j_res


@msgWrapper(ldt=20240831,s_func_remark='部门获取门店权限')
def ddGetPermissionBraid(j_args):
    return ddGetPermissionBraidMain(j_args)


@msgWrapper(ldt=20240228,s_func_remark='员工菜单信息')
def authMenuList(userid:int):
    j_res = authMenuListMain(userid)
    j_res.update({'userid':userid})
    return j_res


@msgWrapper(ldt=20240228,s_func_remark='员工按钮权限')
def authUserButton(userid:int):
    j_res = authUserButtonMain(userid)
    j_res.update({'userid':userid})
    return j_res


@msgWrapper(ldt=20240615,s_func_remark='推送JOB任务')
def postJob(j_args={}):
    jobid = j_args.get('jobid',0)
    j_res = postJobMain(jobid,j_args)
    logs = threadLogs(from_code='postJob', key_code= jobid,args_in= j_args,args_out= j_res)
    logs.start()
    j_res['params'] = j_args
    return j_res


# @msgWrapper(ldt=20240314,s_func_remark='商品档案信息')
# def prdInfo(jobid:int,userid,j_args={}):
#     j_res = postJobMain(jobid,j_args)
#     j_res['params'] = j_args
#     j_res.update({'jobid':jobid})
#     logs = threadLogs(thread_id = jobid ,thread_name = userid,fac = j_res['Fac'],args_dict = j_res)
#     logs.start()
#     return j_res

