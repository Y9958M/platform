# -*- coding:utf-8 -*-
import datetime
import time
import traceback
from weakref import WeakKeyDictionary
from eventlet import tpool
from nameko.dependency_providers import DependencyProvider
from nameko.rpc import rpc

from cmm import HandleLog, msgWrapper, threadLogs
# from common.fac import commonQuery, commonRedis,commonBillid,commonBillInfo,authLogin, authUserButton, authMenuList, postJob,ddLogin,ddGetPermissionBraid
from common.foo import (commonQueryMain,commonRedisMain,cmmBillidMain,cmmBillInfoMain,cmmBillDelMain
                  ,authLoginMain,ddLoginMain, authUserButtonMain, authMenuListMain,postJobMain
                  ,ddGetPermissionBraidMain,ddGetPermissionButtonMain)
log = HandleLog('Service',i_c_level=30,i_f_level=30)
# author  :don
# date    :2024-02-02
# description: 提供中台微服务提供 传输数据用 JSON


class LoggingDependency(DependencyProvider):

    def __init__(self):
        self.timestamps = WeakKeyDictionary()

    def worker_setup(self, worker_ctx):

        self.timestamps[worker_ctx] = datetime.datetime.now()

        service_name = worker_ctx.service_name
        method_name = worker_ctx.entrypoint.method_name

        log.info("%s.%s starting"%(service_name, method_name))

    def worker_result(self, worker_ctx, result=None, exc_info=None):

        service_name = worker_ctx.service_name
        method_name = worker_ctx.entrypoint.method_name

        if exc_info is None:
            status = "completed"
        else:
            status = "errored"
            log.error(traceback.print_tb(exc_info[2]))

        now = datetime.datetime.now()
        worker_started = self.timestamps.pop(worker_ctx)
        elapsed = (now - worker_started).seconds

        log.info("%s.%s %s after %ds"%(service_name, method_name, status, elapsed))

class PlatformService(object):
    # 定义微服务名称 
    name = "YM"
    log = LoggingDependency()

    @rpc
    def computation_bound(self):
        # 该任务一经发起会被不停重试，消耗计算资源
        start = time.time()
        while True:
            if time.time() - start > 300:
                break

    @rpc
    def computation_bound_sleep(self):
        # 使用 sleep 交出控制流让框架能够发送心跳
        start = time.time()
        while True:
            if int(time.time() - start) % 5 == 0:
                time.sleep(0.2)

            if time.time() - start > 300:
                break

    @rpc
    def computation_bound_tpool(self):
        # 使用 tpool 切换为线程运行
        return tpool.execute(self.computation_bound())

    @rpc
    def raise_exception(self):
        raise Exception()


    @rpc
    def hello_world(self, msg):
        log.debug('hello,i am Platform been called by customer 消费者 ,返回消息：{}'.format(msg))
        return f"Hello World!I Am {self.name}: {msg} from Platform producer! 确认已连接"

    @rpc    # 公共查询 在API前端转 DICT 
    @msgWrapper(ldt=20240615,s_func_remark='通用【查询】对外服务')
    def cQ(self, j_args):
        j_res = commonQueryMain(j_args)
        logs = threadLogs(from_code='commonQuery', key_code= j_args.get('sqlid',''),args_in= j_args,args_out= j_res)
        logs.start()
        j_res['params'] = j_args
        return j_res


    # @rpc    # 公共更新  313起就没了
    # def cU(self, j_args):
    #     return msgJson(commonUpdate(j_args))

    @rpc
    @msgWrapper(ldt=20240615,s_func_remark='推送JOB任务')
    def cPostJob(self,j_args={}):   # jobid,userid,j_args
        jobid = j_args.get('jobid',0)
        j_res = postJobMain(jobid,j_args)
        logs = threadLogs(from_code='postJob', key_code= jobid,args_in= j_args,args_out= j_res)
        logs.start()
        j_res['params'] = j_args
        return j_res

    @rpc
    @msgWrapper(ldt=20240228,s_func_remark='通用【单号】')
    def cBillid(s_bill_key:str,bltid=1):
        j_res = cmmBillidMain(s_bill_key, bltid=1)
        j_res['params'] = {'bill_key':s_bill_key,'bltid':bltid}
        return j_res


    @rpc    # 默认查询，s_act == del 删除状态0 1 单据
    @msgWrapper(ldt=20240304,s_func_remark='通用【单号信息】')
    def cBillInfo(self,s_billid:str,s_act='query'): 
        if s_act == 'query':
            j_res = cmmBillInfoMain(s_billid)
        elif s_act.lower() == 'del':
            j_res = cmmBillDelMain(s_billid)
        else:
            j_res = {'msg':'未配对通用单据动作'}
        j_res.update({'billid':s_billid})
        return j_res


    # AUTH -------------------- 登录要验证 平台标识 code_from authMenuList 可以限制访问 ----------------------------------------------------------
    @rpc    
    @msgWrapper(ldt=20240615,s_func_remark='检查登陆')
    def cAuthLogin(self,j_args):
        j_res = authLoginMain(j_args)
        s_user = j_args.get('phone_no',0) if j_args.get('phone_no',0) else j_args.get('user_code','-99') 
        logs = threadLogs(from_code='authLogin', key_code= s_user,args_in= j_args,args_out= j_res)
        logs.start()
        j_res['params'] = j_args
        return j_res


    @rpc    
    @msgWrapper(ldt=20240228,s_func_remark='员工菜单信息')
    def cAuthMenu(self,userid:int):
        j_res = authMenuListMain(userid)
        j_res.update({'userid':userid})
        return j_res


    @rpc  
    @msgWrapper(ldt=20240228,s_func_remark='员工按钮权限')  
    def cAuthUserButton(self,userid:int):
        j_res = authUserButtonMain(userid)
        j_res.update({'userid':userid})
        return j_res

    # DD  ----------------------------
    @rpc   
    @msgWrapper(ldt=20240615,s_func_remark='钉钉-登陆 课组权限') 
    def cDdLogin(self,j_args):
        j_res = ddLoginMain(j_args)
        s_user = j_args.get('phone_no',0) if j_args.get('phone_no',0) else j_args.get('user_code','-99') 
        logs = threadLogs(from_code='authLogin', key_code= s_user,args_in= j_args,args_out= j_res)
        logs.start()
        j_res['params'] = j_args
        return j_res
    
    @rpc
    @msgWrapper(ldt=20240831,s_func_remark='钉钉-门店权限')
    def cDdGetPermissionBraid(self,j_args):
        return ddGetPermissionBraidMain(j_args)

    @rpc
    @msgWrapper(ldt=20240831,s_func_remark='钉钉-按钮权限')
    def cDdGetPermissionButton(self,j_args):
        return ddGetPermissionButtonMain(j_args)

    # RsMdmV1Bra ----------------------------
    @rpc    
    @msgWrapper(ldt=20240615,s_func_remark='通用【缓存】入参 redis_type redis_db rs_name rs_key rs_val proj_name sqlid time_expire')
    def cR(self,j_args):
        j_res = commonRedisMain(j_args)
        logs = threadLogs(from_code='commonQuery', key_code= j_args.get('sqlid',''),args_in= j_args,args_out= j_res)
        logs.start()
        j_res['params'] = j_args
        return j_res
    
    # RETURN ---------------------------------------


# FlaskPooledClusterRpcProxy接受所有以前缀为前缀的 nameko 配置值。此外，它还公开了其他配置选项：NAMEKO_

# NAMEKO_INITIAL_CONNECTIONS (int, default=2)- 要创建的与 Nameko 集群的初始连接数
# NAMEKO_MAX_CONNECTIONS (int, default=8)- 引发错误之前要创建的到 Nameko 群集的最大连接数
# NAMEKO_CONNECT_ON_METHOD_CALL (bool, default=True)- 是否应在访问服务时加载与服务的连接（False）或在服务上调用方法时加载（True）
# NAMEKO_RPC_TIMEOUT（int， default=None） - 尝试调用服务 RPC 方法时引发错误之前的默认超时
# NAMEKO_POOL_RECYCLE（int，default=None） - 如果指定，则早于此间隔（以秒为单位）的连接将在签出时自动回收。此设置对于通过代理（如 HAProxy）进行连接的环境非常有用，该代理会在指定的时间间隔后自动关闭连接。

