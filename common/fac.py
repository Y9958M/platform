# -*- coding:utf-8 -*-
from .cmm import threadLogs,msgWrapper
from .foo import commonQueryMain,commonRedisMain,authLoginMain, authUserButtonMain, authMenuListMain,postJobMain,cmmBillidMain,cmmBillInfoMain,cmmBillDelMain

# author  :don
# date    :20240202
# description: 接待入口 包装层面 不处理入参检查 通用 JOB功能 项目区分


@msgWrapper(ldt=20240313,s_func_remark='通用【查询】对外服务')
def commonQuery(args_dict):
    j_res = commonQueryMain(args_dict)
    j_res['params'] = args_dict
    logs = threadLogs(thread_id= j_res.get('userid',-99),thread_name= j_res.get('sqlid','NULL'),fac= "commonQuery",args_dict= j_res)
    logs.start()
    return j_res


# @msgWrapper(ldt=20240228,s_func_remark='通用【更新】')
# def commonUpdate(args_dict):
#     j_res = commonUpdateMain(args_dict)
#     j_res['params'] = args_dict
#     logs = threadLogs(thread_id= j_res.get('userid',-99),thread_name= j_res.get('sqlid','NULL'),fac= "commonQuery",args_dict= j_res)
#     logs.start()
#     return j_res


@msgWrapper(ldt=20240228,s_func_remark='通用【缓存】入参 redis_type redis_db rs_name rs_key rs_val proj_name sqlid time_expire')
def commonRedis(args_dict):
    j_res = commonRedisMain(args_dict)
    j_res['params'] = args_dict
    logs = threadLogs(thread_id= j_res.get('userid',-99),thread_name= j_res.get('rs_name','rs_name'),fac= "commonQuery",args_dict= j_res)
    logs.start()
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

@msgWrapper(ldt=20240228,s_func_remark='检查登陆')
def authLogin(userid,api_no:int):
    j_res = authLoginMain(userid)
    j_res['params'] = {'userid':userid,'api_no':api_no}
    logs = threadLogs(thread_id= j_res.get('api_no',-99),thread_name= userid,fac= "commonQuery",args_dict= j_res)
    logs.start()
    return j_res


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


@msgWrapper(ldt=20240228,s_func_remark='推送JOB任务')
def postJob(jobid:int,userid,j_args={}):
    j_res = postJobMain(jobid,j_args)
    j_res['params'] = j_args
    j_res.update({'jobid':jobid})
    logs = threadLogs(thread_id = jobid ,thread_name = userid,fac = j_res['Fac'],args_dict = j_res)
    logs.start()
    return j_res
