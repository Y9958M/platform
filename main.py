
import logging,colorlog
import os,time
import threading
import decimal
import json
import redis
import sqlalchemy
from logging.handlers import RotatingFileHandler
from datetime import date, datetime, timedelta
from sqlalchemy.pool import QueuePool
import pandas as pd,numpy as np
from config import CLIENT,DB_LINK,VER,SID,ADMIN,PROJECT,MESSAGE


logging._srcfile = None
logging.logThreads = 0
logging.logMultiprocessing = 0
logging.logProcesses = 0
logging.thread = None  # type: ignore
log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')  # log_path为存放日志的路径
if not os.path.exists(log_path): os.mkdir(log_path)  # 若不存在logs文件夹，则自动创建
s_log_file = os.path.join(log_path,f"mp-{datetime.now().strftime('%Y%m%d')}.log")


rs = redis.Redis(connection_pool=redis.ConnectionPool(
    host    =   DB_LINK['REDIS']['HOST'],
    password =  DB_LINK['REDIS']['PWD'],
    port =      DB_LINK['REDIS']['PORT'],
    db =        DB_LINK['REDIS']['DB'],
    decode_responses=True,
    encoding='utf-8'))


def setGlobal()->dict:
    ce = sqlalchemy.create_engine(f"mysql+pymysql://{DB_LINK['YM']['USER']}:{DB_LINK['YM']['PWD']}@{DB_LINK['YM']['HOST']}:{DB_LINK['YM']['PORT']}/platform")
    s_ = f"SELECT json_values FROM set_global WHERE project_name = 'GLOBAL' AND project_key = 'SETUP';"
    df = pd.read_sql_query(s_,ce)['json_values'].head(1)
    if df.shape[0] == 0:
        raise Exception(f"SELECT json_values FROM set_global WHERE project_name = 'GLOBAL' AND project_key = 'SETUP'")
    else:
        j_ = eval(df.to_dict()[0])
    if 'VER' not in j_.keys():
        raise Exception(f"Yao Ming tell you: set_global > SETUP > json_values > VER is NEED! ")
    elif j_['VER'] != VER:
        raise Exception(f"Yao Ming tell you: PROJECT:{VER} DB:{j_['VER']} VER IS NOT MARRY ! ")
    else:
        print(f"{'-' * 24} platform {'-' * 24}")
        print(j_)
    return j_


def engine(DB='platform',LINK=""):
    LINK = LINK if LINK else 'YM'
    JDBC ={'MYSQL':'mysql+pymysql','MSSQL':'mssql+pymssql'}
    PARM ={'MYSQL':'','MSSQL':'?charset=cp936'}
    s_ = f"{JDBC[DB_LINK[LINK]['TYPE']]}://{DB_LINK[LINK]['USER']}:{DB_LINK[LINK]['PWD']}@{DB_LINK[LINK]['HOST']}:{DB_LINK[LINK]['PORT']}/{DB}{PARM[DB_LINK[LINK]['TYPE']]}"
    return sqlalchemy.create_engine(s_, poolclass=QueuePool, max_overflow=10, pool_size=24, pool_timeout=30, pool_recycle=3600)


# 初始化配置 数据从后台取 初始化的时候 取项目库JSON数据# 连接后台 启动级异常 不需要返回 直接记日志
class HandleLog:
    def __init__(self,s_name, s_path=s_log_file, i_c_level = 60 - SID*10, i_f_level = 60 - SID*10):
        self.logger = logging.getLogger(s_name) # 创建日志记录器
        self.logger.setLevel(logging.DEBUG)
        # self.__logger = logging.getLogger() 
        formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s %(name)6s: %(message_log_color)s%(message)s',
        datefmt='%y%m%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG':    'black',
            'INFO':     'cyan',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={'message':{
            'DEBUG':    'light_black',
            'INFO':     'light_cyan',
            'WARNING':  'light_yellow',
            'ERROR':    'light_red',
            'CRITICAL': 'light_purple'
        }},
        style='%')

        #设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(i_c_level)

        #设置文件日志
        fh = RotatingFileHandler(filename=s_path, mode="w", maxBytes=5*1024*1024, backupCount=5,encoding='utf-8')
        formatter_file = logging.Formatter('%(asctime)s %(name)s %(levelname)9s: %(message)s', datefmt='%a %y%m%d %H:%M:%S')
        fh.setFormatter(formatter_file)
        fh.setLevel(i_f_level)

        self.logger.propagate = False
        if not self.logger.handlers: # 防止日志重复打印 logger.propagate 布尔标志, 用于指示消息是否传播给父记录器
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)
    
    def debug(self,message,title=''):
        self.logger.debug(f"{title}:{message}" if title else message)

    def info(self,message,title=''):
        self.logger.info(f"{title}:{message}" if title else message)

    def warning(self,message,title=''):
        self.logger.warning(f"{title}:{message}" if title else message)

    def error(self,message,title=''):
        self.logger.error(f"{title}:{message}" if title else message)

    def cri(self,message,title=''):
        self.logger.critical(f"{title}:{message}" if title else message)


# -*- 把Date、DateTime类型数据转换成兼容Json的格式 -*-  json.dumps(result,cls=DateEncoder.DateEncoder) # 调用自定义类
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj,sqlalchemy.engine.row.Row):
            return list(obj)
        elif isinstance(obj,sqlalchemy.engine.row.RowMapping):
            return dict(obj)
        elif isinstance(obj,sqlalchemy.engine.result.RMKeyView):
            return list(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def msgJson(data):
    return json.dumps(data,cls=DateEncoder,ensure_ascii=False)


# 要区分一下 查询 JOB 单据 job_custom_logs 
class threadLogs(threading.Thread):
    def __init__(self,thread_id,thread_name:str,fac:str,args_dict={}):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.args_dict = args_dict
        self.fac = fac

    def run(self):
        FAC = self.fac
        LOGS = {
    "commonQuery":    "insert into log_common_query(userid,sqlid,parm_json)values(%s,%s,%s)",
    "commonUpdate":   "insert into log_common_update(userid,sqlid,parm_json)values(%s,%s,%s)",
    "commonRedis":    "insert into log_common_redis(userid,redis_name,parm_json)values(%s,%s,%s)",
    "commonBill":     "insert into log_common_bill(userid,billid,parm_json)values(%s,%s,%s)",
    "authLogin":      "insert into log_auth_login(api_no,userid,parm_json)values(%s,%s,%s)",
    }
        time.sleep(3)
        conn = engine().connect()
        try:
            if FAC in LOGS:
                args = self.args_dict
                if FAC in ['commonQuery'] and 'data' in args:
                    if 'datalist' in args['data']:
                        args['tip'] ="3s del data_list!"
                        del args['data']['datalist']
                conn.exec_driver_sql(LOGS[FAC],(self.thread_id,self.thread_name,msgJson(args)))
                conn.commit()
            else:
                conn.exec_driver_sql("insert into log_def(threadid,thread_name,parm_json)values(%s,%s,%s)",
                (self.thread_id,self.thread_name,msgJson(self.args_dict)))
                conn.commit()
        except Exception as e:
            print("threadLogs",e)


GLOBAL = setGlobal()
