# -*- coding:utf-8 -*-
from main import GLOBAL, MESSAGE, SID, DB_LINK,HandleLog,engine,rs

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-02-02
# description: 数据库存相关操作 明确传入的值



def checkSqlContext(sql_context):
    message = MESSAGE.copy()
    message['fun'] = 'fun checkSqlContext'

    info = f' WARNING 有破坏活动！ \n{sql_context}'
    s_sql = sql_context.lower()
    if s_sql.find('delete ') >= 0:
        message.update({'msg':'delete {}'.format(info)})
        log.warning(message)
        return message
    elif s_sql.find('update ') >=0:
        message.update({'msg':'update {}'.format(info)})
        log.warning(message)
        return message
    elif s_sql.find('truncate ') >=0:
        message.update({'msg':f'truncate {info}'})
        log.warning(message)
        return message
    elif s_sql.find(' into ') >=0:
        message.update({'msg':f'into {info}'})
        log.warning(message)
        return message
    elif s_sql.find('drop ') >=0:
        message.update({'msg':f'drop {info}'})
        log.warning(message)
        return message
    elif s_sql.find('alter ') >=0:
        message.update({'msg':f'alter {info}'})
        log.warning(message)
        return message
    elif s_sql.find(' --') >=0:
        message.update({'msg':f' -- {info}'})
        log.warning(message)
        return message
    else:
        message.update({'code':200})
        return message

# 把文本变为LIST，输入STR，输出LIST ,换行
def sqlContextToList(sql_str):
    res = iter(sql_str)
    each_str = ''
    sql_list = []
    sql_paramter_dict = {}
    for x in res:
        each_str += x
        if x =='\n':
            sql_list.append(each_str)
            each_str = ''
        # 直接给字典
        elif x == '}' and each_str[0] == '{':
            try:
                sql_paramter_dict = eval(each_str)
                sql_list.append(sql_paramter_dict)
            except:
                return None
            finally:
                each_str =''
                sql_paramter_dict = {}
        elif x ==';':
            sql_list.append(each_str)
            return sql_list
    sql_list.append(each_str)
    log.debug(sql_list,'sqlContextToList')
    return sql_list

# 定义一个函数，用来匹配外部DICT,入参，LIST和DICT，输出STR
def swapContent(quary_list,paramter_dict):
    message = MESSAGE.copy()
    message['fun'] = 'utils swapContent'
    log.debug(paramter_dict,'paramter_dict')

    if not quary_list:
        message.update({'msg':f"转换失败 检查 sql_context "})
        return message

    sql_result =[]
    for x in quary_list:
        if isinstance(x, dict):
            if 'k' not in x or 'v' not in x:
                message.update({'msg':'未配置k和v 示例:"k":"id","v":"AND id = ? "'})
                return message  # 解决字典没有关键字  
            keys = str(x['k'])
            if keys in paramter_dict:
                #这里要替换数据 如果是 值 为''
                sk = str(paramter_dict[keys])
                # 如果必传的值为空 要返回
                if 'n' in x:
                    if x['n']:
                        if sk =='' or sk == 'None' or sk == '[]' or sk =='()':
                            message.update({'msg':'必传字段 不能为 %s'%sk})
                            return message
                if sk =='' or sk == 'None' or sk == '[]' or sk =='()':
                    pass
                else:
                    sql_result.append(x['v'].replace('?',sk))
            elif 'd' in x:
                sql_result.append(x['v'].replace('?',x['d']))
            elif 'n' in x:
                if  isinstance(x['n'], bool):
                    if x['n']:
                        message.update({'msg':'有必传字段 %s'%keys})
                        return message
                else:
                    message.update({'msg':'n 参数规范： True False 不带引号'})
                    return message
            else:
                continue
        elif isinstance(x, str):
            if x in [' \r\n','\t\r\n','\r\n']:
                continue
            else:
                sql_result.append(x)   
        else:
            continue

    if len(sql_result) < 1:
        message.update({'msg':'sql_context 生成的 执行语句为空'})
        return message
    s_sql = ''.join(sql_result)    
    if s_sql.find('}') >=0:
        message.update({'msg':'sql_context 替换 必须单独一行并置顶 不要加空格或TAB'})
        return message
    
    message.update({'code':200,'data':s_sql})
    return message


# 检查数据库连接
def ckDbLink(s_project='YM'):   # 传入的项目缩写
    message = MESSAGE.copy()
    message['fun'] = 'fun ckDbLink'
    log.debug(s_project,'ckDbLink 0')

    if s_project == 'YM':
        s_db_type = 'MYSQL'
        s_db =      'platform'
    elif s_project not in DB_LINK['YM']['USE'] and s_project not in DB_LINK:
        message.update({'msg':f"{s_project} 需要在DB_LINK中对应"})
        return message
    elif s_project in DB_LINK['YM']['USE']:
        s_db_type = DB_LINK['YM']['TYPE']
        s_db =      DB_LINK['YM']['USE'][s_project]
        s_project = 'YM'
    elif 'DB' not in DB_LINK[s_project]:
        message.update({'msg':f"{s_project} 需要在DB_LINK中配置DB"})
        return message
    else:
        s_db_type = DB_LINK[s_project]['TYPE']
        s_db =      DB_LINK[s_project]['DB']
        s_project = s_project
    message.update({'code':200,'data':{'TYPE':s_db_type,'DB':s_db,'PROJECT':s_project}})
    log.debug(s_project,'ckDbLink 1')
    return message


# 检查更新要求
def ckUpInfo(sid:int,s_project:str,s_db:str):   # 传入的项目缩写
    message = MESSAGE.copy()
    message['fun'] = 'fun ckUpInfo'

    jl_cuda = GLOBAL['CUDA']    # jl_字典的子项是列表
    if sid != SID: message.update({'msg':f"sid 不一致 传入标识 {sid} 环境标识 {SID}"})
    elif s_project not in jl_cuda.keys(): message.update({'msg':f"项目全局 set_global 未配置 传入 {s_project} "})
    elif s_db not in jl_cuda[s_project]: message.update({'msg':f"CUDA中 {s_project} 未配置 {s_db}"})
    else:message.update({'code':200})
    return message


# 平台 按系统的通用查询
def cmmFetchone(sqlid:str,s_table='common_query')->dict:
    message = MESSAGE.copy()
    message['fun'] = 'fun cmmFetchone'

    with engine().connect() as conn:
        s_= f"SELECT project,sql_context,sql_name,remark FROM {s_table} WHERE sqlid ='{sqlid}';"
        try:
            res = conn.exec_driver_sql(s_)
            l_ds = res.fetchone()
            if l_ds:message.update({'project':l_ds[0],'sql_context':l_ds[1],'sql_name':l_ds[2],'remark':l_ds[3],'code':200})
            else:message.update({'msg':f"{s_table} 中 SQLID {sqlid} 未查询到对应记录！",'remark':s_})
        except Exception as e:
            message['msg'] = str(e)
            log.error(message)
            return message
    return message


# MYSQL 拼接时用的时候处理 不处理kv
def cmmQueryMysql(s_db:str,s_project:str,s_sql:str,sqlid:str,i_page_num=1,i_page_size=1000)->dict:
    message = MESSAGE.copy()
    message['fun'] = 'fun cmmQueryMysql'
    message['sqlid'] = sqlid
    log.debug(f">>> {message['fun']} 执行语句 :{s_sql}")

    i_total = 0
    s_total_sql = f"select count(*) AS total from ({s_sql}) t1"
    with engine(s_db,s_project).connect() as conn:
        try:
            res = conn.exec_driver_sql(s_total_sql)
            i_total = res.fetchone()[0]
        except Exception as e:
            message.update({'msg':str(e)})
            log.error(message)
            return message
        if i_total == 0:
            message.update({'data':{'fields':[],'datalist':[],'total':i_total,'pageNum':i_page_num,'pageSize':i_page_size},'code':200,'msg':f"> total:{i_total}"})
            return message
        elif i_total > i_page_size:
            s_sql = f"{s_sql} LIMIT {(i_page_num-1) * i_page_size},{i_page_size}"
        try:
            res = conn.exec_driver_sql(s_sql)
            i_rc = res.rowcount
            l_ds = res.fetchall()
            l_field = list(res.keys())
            message.update({'data':{'datalist':l_ds,'fields':l_field,'total':i_total,'pageNum':i_page_num,'pageSize':i_page_size},'code':200,"count":i_rc,'msg':f"> total:{i_total}"})   
        except Exception as e:
            message.update({'remark':s_sql.replace('\r\n',' '),'msg':str(e)})
            log.error(message)
            return message
    log.debug(f"<<< {message['fun']} 命中数：{i_rc}")
    return message


# MYSQL 拼接时用的时候处理 不处理kv
def cmmExecMysql(s_db:str,s_project:str,s_sql:str,sqlid:str)->dict:
    message = MESSAGE.copy()
    message['fun'] = 'fun cmmExecMysql'
    message['sqlid'] = sqlid
    log.debug(f">>> {message['fun']} 执行语句 :{s_sql}")

    with engine(s_db,s_project).connect() as conn:
        try:
            res = conn.exec_driver_sql(s_sql)
            i_rc = res.rowcount
            message.update({'code':200,"count":i_rc,'msg':f"> 更新数：{i_rc}"})   
        except Exception as e:
            message.update({'remark':s_sql.replace('\r\n',' '),'msg':str(e)})
            log.error(message)
            return message
    log.debug(f"<<< {message['fun']} 更新数：{i_rc}")
    return message

# MSSQL KV
def commonQueryMssqlKV(s_db:str,s_project:str,s_sql:str,sqlid:str)->dict:
    message = MESSAGE.copy()
    message['fun'] = 'fun commonQueryMssqlKV'
    message['sqlid'] = sqlid
    log.debug(f">>> {message['fun']} MSSQL {s_project} 执行:{s_sql}")
    i_rc = 0
    i_total = 0
    s_total_sql = f"select count(*) AS total from ({s_sql}) t1"
    with engine(s_db,s_project).connect() as conn:

        try:
            res = conn.exec_driver_sql(s_sql)
            # dbcur.execute(s_sql.encode('cp936'))
            l_ds = res.mappings().all()
            i_rc = res.rowcount     #<<
            message.update({'data':{'datalist':l_ds},'code':200,'count':i_rc,'msg':f">>> {message['fun']} 命中数:{i_rc}"})
        except Exception as e:
            message.update({'remark':s_sql.replace('\r\n',' ').replace('\t',' '),'msg':f"{str(e)}"})
            log.error(message)
            return message
    log.debug(f"<<< {message['fun']} MS命中数：{rc}")            
    return message



# REDIS 执行 具体功能 明确入参
def cmmRedis(redis_name:str,time_expire=0,fields_list =[],data_list=[],redis_db= 0):
    message = MESSAGE.copy()
    message['fun'] = 'commonJobs_fun cmmRedis'
    log.debug(f">>> {message['fun']} name {redis_name} :{fields_list}")

    pipe = rs.pipeline()
    _s = len(fields_list)
    rc = 0
    if _s == 0:
        rs_val = data_list[0]
        if rs_val:
            if isinstance(rs_val, datetime):
                rs_val = rs_val.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(rs_val, date):
                rs_val = rs_val.strftime("%Y-%m-%d")
            elif isinstance(rs_val, decimal.Decimal):
                rs_val = float(rs_val)
        else:
            message.update({'msg':f" REDIS STR 未传入 rs_cal"})
            return message            
        rs.set(redis_name,rs_val)
        rs.expire(redis_name,time_expire)
        message.update({'count':1,'code':200,'msg':f"> DB = {Db['DB']} name = {redis_name} value {rs_val} time_expire={time_expire} 成功"})
        return message
    if redis_name not in fields_list:
        message.update({'msg':f" 关键字段 {redis_name} 在 table_name 中设置 与字段不配 {fields_list}"})
        return message
    
    try:
        _i = fields_list.index(redis_name)
        for l in data_list:
            key_info =f"{redis_name}:{l[_i]}"
            _dic = {}
            for i in range(_s):
                if l[i]:# 需要转换
                    if isinstance(l[i], datetime):
                        _dic[fields_list[i]] = l[i].strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(l[i], date):
                        _dic[fields_list[i]] = l[i].strftime("%Y-%m-%d")
                    elif isinstance(l[i], decimal.Decimal):
                        _dic[fields_list[i]] = float(l[i])
                    else:
                        _dic[fields_list[i]] = l[i]
            pipe.hmset(key_info,_dic)
            rc += 1
            if time_expire:
                pipe.expire(key_info, time_expire)
    except Exception as e:
        message.update({'msg':f" REDIS 转化失败 {str(e)}"})
        return message
    try:
        pipe.execute()
        # log.debug("execute")
        message.update({'count':rc,'code':200,'msg':f"> DB = {Db['DB']} KEY = {redis_name} time_expire={time_expire} rc {rc} 成功"})
        return message
    except Exception as e:
        message.update({'msg':f" REDIS {Db['HOST']} 连接失败  {str(e)}"})
        return message   


# 检查重复调用的
def canInvokeTimeBool(api:str,times=60,proj_name="REDIS"):
    try:
        if rs.exists(api):
            return True
        else:
            rs.set(api,times)
            rs.expire(api, times)
            return False
    except Exception as e:
        log.error(str(e))

# 检查参数
def checkCommonRedisArgs(args_dict):
    _b = True
    if 'redis_db' not in args_dict:
        pass
        # message.update({'msg':'need redis_db '})
    elif 'rs_name' not in args_dict:
        pass
        # message.update({'msg':'need rs_name '})
    else:_b = False
    return _b