# -*- coding:utf-8 -*-
import datetime
import time
import traceback
from weakref import WeakKeyDictionary
from eventlet import tpool
from nameko.dependency_providers import DependencyProvider
from nameko.rpc import rpc

from common.cmm import HandleLog, msgJson
from common.fac import commonQuery, commonRedis,commonBillid,commonBillInfo,authLogin, authUserButton, authMenuList, postJob

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
    def cQ(self, j_args):
        return msgJson(commonQuery(j_args))

    # @rpc    # 公共更新  313起就没了
    # def cU(self, j_args):
    #     return msgJson(commonUpdate(j_args))

    @rpc
    def cPostJob(self,jobid,userid,j_args):
        return msgJson(postJob(jobid,userid,j_args))

    @rpc
    def cBillid(self,s_bill_key:str,bltid:int): 
        return msgJson(commonBillid(s_bill_key,bltid))

    @rpc    # 默认查询，s_act == del 删除状态0 1 单据
    def cBillInfo(self,s_billid:str,s_act='query'): 
        return msgJson(commonBillInfo(s_billid,s_act))
    
    # AUTH -------------------- 登录要验证 平台标识 code_from authMenuList 可以限制访问 ----------------------------------------------------------
    @rpc    
    def cAuthLogin(self,userid:str,code_from:str):
        return msgJson(authLogin(userid,code_from))

    @rpc    
    def cAuthMenu(self,userid:int):
        return msgJson(authMenuList(userid))

    @rpc    
    def cAuthUserButton(self,userid:int):
        return msgJson(authUserButton(userid))

    # RsMdmV1Bra ----------------------------
    @rpc    
    def cR(self,j_args):
        return msgJson(commonRedis(j_args))
    
    # RETURN ---------------------------------------


# FlaskPooledClusterRpcProxy接受所有以前缀为前缀的 nameko 配置值。此外，它还公开了其他配置选项：NAMEKO_

# NAMEKO_INITIAL_CONNECTIONS (int, default=2)- 要创建的与 Nameko 集群的初始连接数
# NAMEKO_MAX_CONNECTIONS (int, default=8)- 引发错误之前要创建的到 Nameko 群集的最大连接数
# NAMEKO_CONNECT_ON_METHOD_CALL (bool, default=True)- 是否应在访问服务时加载与服务的连接（False）或在服务上调用方法时加载（True）
# NAMEKO_RPC_TIMEOUT（int， default=None） - 尝试调用服务 RPC 方法时引发错误之前的默认超时
# NAMEKO_POOL_RECYCLE（int，default=None） - 如果指定，则早于此间隔（以秒为单位）的连接将在签出时自动回收。此设置对于通过代理（如 HAProxy）进行连接的环境非常有用，该代理会在指定的时间间隔后自动关闭连接。

