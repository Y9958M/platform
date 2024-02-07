
from main import SID,MESSAGE,HandleLog
from .fun import *

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2022-09-23
# description: 组装好模块 调用fun中的数据和utils中的逻辑
# 通用查询中 表和SQLID对应 是否有更好的方法 


# 通用查询 no KV
def commonQueryMain(j_args)->dict:
    message = MESSAGE.copy()
    message['fun'] = 'foo commonQueryMain'
    log.debug(f">> {message['fun']} 通用查询 入参 {j_args}")

    # 初始返回信息格式
    message.update({'msg':'通用查询','remark':'','data':{
        'datalist': [],
        'count':    0,
        'fields':   [],
        'pageNum':1,'pageSize':100,'total':0}})

    if 'sqlid' not in j_args:
        message.update({'msg':"need sqlid"})
        return message
    else:
        sqlid = j_args['sqlid']
        i_page_num  = j_args['pageNum']  if 'pageNum'  in j_args else 1     # 第几页
        i_page_size = j_args['pageSize'] if 'pageSize' in j_args else 10    # 一次查询的数量
        message['data']['pageNum']  = i_page_num
        message['data']['pageSize'] = i_page_size
        message['data']['total']    = 0
        message['sqlid']   = sqlid
    
    j_ = dict() # 查询平台库 platform
    j_.update(cmmFetchone(sqlid,'common_query'))
    if j_['code'] > 200:return j_
    else:
        sql_context =   j_['sql_context']
        s_project   =   j_['project']
        message['sql_name'] = j_['sql_name']
        message['remark']   = j_['remark']
        
    j_.clear()  # check sql_context 防注入检查'
    j_.update(checkSqlContext(sql_context))
    if  j_['code'] > 200:
        j_['sqlid'] = sqlid
        return j_

    j_.clear()  # 检查 DB_LINK 连接
    j_.update(ckDbLink(s_project))
    if  j_['code'] >200:
        j_['sqlid'] = sqlid
        return j_
    else:j_db_info = j_['data']

    # 处理 sql_context    
    l_sql = sqlContextToList(sql_context)
 
    j_.clear()  # 查询拼装
    j_.update(swapContent(l_sql,j_args))
    if  j_['code'] >200:
        j_['sqlid'] = sqlid
        return j_
    else:s_sql = j_['data']

    if   j_db_info['TYPE'] == 'MYSQL':
        message.update(cmmQueryMysql(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid,i_page_num,i_page_size)) 
    elif j_db_info['TYPE'] == 'MSSQL':
        message.update(commonQueryMssql(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid))    # 暂时不支持分页
    elif j_db_info['TYPE'] == 'ORACLE':
        message.update(cmmExecOra(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid))
    else:
        message.update({'msg':f"查询失败 未匹配TYPE: {j_db_info['TYPE']}"})
    return message


# 通用更新 只能在支持的表中处理
def commonUpdateMain(j_args):
    message = MESSAGE.copy()
    message['fun'] = 'foo commonUpdateMain'
    log.debug(f">> {message['fun']} 通用更新模块 DO 只能在支持的表中处理 {j_args}")

    if 'sid' not in j_args:
        message.update({'msg':"need sid"})
        return message
    else:
        sid = j_args['sid']

    if 'sqlid' not in j_args:
        message.update({'msg':"need sqlid"})
        return message
    else:
        sqlid = j_args['sqlid']

    j_ = dict() # 查询平台库 通用更新 从注册库取 更新有权限
    j_.update(cmmFetchone(sqlid,"common_update"))
    if j_['code'] > 200:return j_
    else:
        sql_context =   j_['sql_context']
        s_project   =   j_['project']
        message['sql_name'] = j_['sql_name']
        message['remark']   = j_['remark']
 
    j_.clear()  # 检查 DB_LINK 连接
    j_.update(ckDbLink(s_project))
    if j_['code'] >200:
        j_['sqlid'] = sqlid
        return j_
    else:j_db_info = j_['data']

    j_.clear()  # 防止超范围的更新
    j_.update(ckUpInfo(sid,j_db_info['PROJECT'],j_db_info['DB']))
    if j_['code'] >200:
        j_['sqlid'] = sqlid
        return j_

    # 处理 sql_context    
    l_sql = sqlContextToList(sql_context)

    j_.clear()  # 查询拼装
    j_.update(swapContent(l_sql,j_args))
    if j_['code'] >200:
        j_['sqlid'] = sqlid
        return j_
    else:s_sql = j_['data']

    if j_db_info['TYPE'] == 'MYSQL':
        message.update(cmmExecMysql(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid)) 
    elif j_db_info['TYPE']== 'MSSQL':
        message.update(cmmExecMssql(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid))
    elif j_db_info['TYPE']== 'ORACLE':
        message.update(cmmExecOra(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid))
    else:
        message.update({'msg':f"{j_db_info['TYPE']} 未能支持 数据库类型"})     
    return message


# 通用缓存数据(存 入参 KEY {字典} 过期时间)
def commonRedisMain(j_args:dict):
    message = MESSAGE.copy()
    message['fun'] = 'foo commonIntoRedis'
    log.debug(f">> {message['fun']} 通用缓存数据(存 入参 KEY 字典 过期时间) \n{j_args}")
    # 检查入参
    j_ = dict()
    if checkCommonRedisArgs(j_args):
        message.update({'msg':'need rs_name'})
        return message
    else:
        project_name=   j_args['project_name'] if 'project_name' in j_args else 'REDIS'
        time_expire =   j_args['time_expire']  if 'time_expire' in j_args else 0
        redis_type  =   j_args['redis_type']   if 'redis_type'  in j_args else 'HASH'
        redis_db    =   j_args['redis_db']     if 'redis_db'    in j_args else 0
        rs_name     =   j_args['rs_name']
        rs_key      =   j_args['rs_key']       if 'rs_key'    in j_args else ""
        rs_val      =   j_args['rs_val']       if 'rs_val'    in j_args else ""

    if redis_type in ['SQLID']:
        data_list = []
        log.debug("SQLID 会调用通用查询")
        if 'sqlid' not in j_args:
            message.update({'msg':"未传入sql_id"})
            return message
        j_ds = {}
        j_ds = commonQueryMain(j_args)
        if j_ds['code'] > 200:return j_ds
        else:
            data_list = j_ds['data']
            fields_list = j_ds['fields_list']

        j_.clear()
        j_ = cmmRedis(redis_name = rs_name,time_expire= time_expire, fields_list= fields_list, data_list= data_list,redis_db= redis_db)
        if j_['code'] > 200:return j_
        else:
            message.update({'code':200,'msg':f"成功更新 缓存库 {redis_db} {rs_name}:XXX  过期时间：{time_expire} 秒",'count':j_['count']})
            return message

    elif redis_type in ['HASH']:
        log.debug(f"HASH rs_key {rs_key} rs_val {rs_val}")
        if rs_val and rs_key:
            j_.clear()
            j_ = cmmRedis(redis_name = rs_name,time_expire= time_expire, fields_list= [rs_key], data_list= [rs_val],redis_db= redis_db)
            if j_['code'] > 200:return j_
            else:message.update({'code':200,'msg':f"成功更新 缓存库 {redis_db} {rs_name},{rs_key},{rs_val}  过期时间：{time_expire} 秒",'count':1})    
        else:message.update({'code':201,'msg':f"缺少参数 rs_key {rs_key} rs_val {rs_val}"})
        return message

    elif redis_type in ['STR']:
        log.debug(f"STR rs_val {rs_val}")
        if rs_val:
            j_.clear()
            j_ = cmmRedis(redis_name = rs_name,time_expire= time_expire, fields_list= [], data_list= [rs_val],redis_db= redis_db)
            if j_['code'] > 200:return j_
            else:message.update({'code':200,'msg':f"成功更新 缓存库 {redis_db} {rs_name}:{rs_val}  过期时间：{time_expire} 秒",'count':1})     
        else:message.update({'code':201,'msg':f"缺少参数 rs_val {rs_val}"})
        return message          

    else:
        message.update({'code':200,'msg':f"传入 {redis_type} 不在范围"})
        return message



