# -*- coding:utf-8 -*-
from .cmm import threadLogs,msgWrapper
from .foo import commonQueryMain,commonUpdateMain,commonRedisMain,authLoginMain, authUserButtonMain, authMenuListMain,postJobMain

# author  :don
# date    :20240202
# description: 接待入口 包装层面 不处理入参检查 通用 JOB功能 项目区分


@msgWrapper(ldt=20240228,s_func_remark='通用【查询】对外服务')
def commonQuery(args_dict):
    j_res = commonQueryMain(args_dict)
    j_res.update(args_dict)
    logs = threadLogs(thread_id= j_res.get('userid',-99),thread_name= j_res.get('sqlid','NULL'),fac= "commonQuery",args_dict= j_res)
    logs.start()
    return j_res


@msgWrapper(ldt=20240228,s_func_remark='通用【更新】')
def commonUpdate(args_dict):
    j_res = commonUpdateMain(args_dict)
    j_res.update(args_dict)
    logs = threadLogs(thread_id= j_res.get('userid',-99),thread_name= j_res.get('sqlid','NULL'),fac= "commonQuery",args_dict= j_res)
    logs.start()
    return j_res


@msgWrapper(ldt=20240228,s_func_remark='通用【缓存】入参 redis_type redis_db rs_name rs_key rs_val proj_name sqlid time_expire')
def commonRedis(args_dict):
    j_res = commonRedisMain(args_dict)
    j_res.update(args_dict)
    logs = threadLogs(thread_id= j_res.get('userid',-99),thread_name= j_res.get('rs_name','rs_name'),fac= "commonQuery",args_dict= j_res)
    logs.start()
    return j_res


@msgWrapper(ldt=20240228,s_func_remark='检查登陆')
def authLogin(userid,api_no:int):
    j_res = authLoginMain(userid)
    j_res.update({'userid':userid,'api_no':api_no})
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
    j_res.update({'jobid':jobid})
    j_res.update(j_args)
    logs = threadLogs(thread_id = jobid ,thread_name = userid,fac = j_res['Fac'],args_dict = j_res)
    logs.start()
    return j_res
