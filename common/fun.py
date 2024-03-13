# -*- coding:utf-8 -*-
import requests
from .cmm import GLOBAL, MESSAGE, SID, DB_LINK,PF_LINK,HandleLog,engine,rs,pd,datetime,date,decimal,json,reverse_dict,l2d

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-02-02
# description: 数据库存相关操作 明确传入的值

def checkSqlContext(sql_context):
    message = MESSAGE.copy()
    message['info']['fun'] = 'fun checkSqlContext'

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
def sqlContextToList(sql_str)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'utils sqlContextToList'
    log.debug(sql_str,'sql_str')

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
            except Exception as e:
                log.error(e)
                return None
            finally:
                each_str =''
                sql_paramter_dict = {}
        elif x ==';':
            sql_list.append(each_str)
            return sql_list
    sql_list.append(each_str)
    log.debug(sql_list,'sqlContextToList')
    message.update({'code':200,'data':sql_list})
    return message


# 定义一个函数，用来匹配外部DICT,入参，LIST和DICT，输出STR
def swapContent(quary_list,paramter_dict)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'utils swapContent'
    log.debug(paramter_dict,'paramter_dict')

    if not quary_list:
        message.update({'msg':"转换失败 检查 sql_context "})
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


# 校验手机号码
def checkPhone(phone)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'checkPhone'
    log.debug(f">>> {message['info']['fun']} 检查通用查询的入参 \n{phone}  ")
    s_phone = str(phone)
    if len(s_phone) == 11 and s_phone[0:1] == '1':
        message.update({'code':200})
    else:
        message.update({'msg':f"请输入正确的手机号 {s_phone}"})
    return message


# 检查数据库连接
def ckDbLink(s_project='YM'):   # 传入的项目缩写
    message = MESSAGE.copy()
    message['info']['fun'] = 'fun ckDbLink'
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


# 平台 按系统的通用查询
def cmmFetchone(sqlid:str,s_table='common_query')->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'fun cmmFetchone'

    with engine().connect() as conn:
        s_= f"SELECT project,sql_context,sql_name,remark FROM {s_table} WHERE sqlid ='{sqlid}';"
        try:
            res = conn.exec_driver_sql(s_)
            l_ds = res.fetchone()
            if l_ds:
                message['code'] = 200
                message.update({'project':l_ds[0],'sql_context':l_ds[1],'sql_name':l_ds[2],'remark':l_ds[3]})
            else:
                message.update({'msg':f"{s_table} 中 SQLID {sqlid} 未查询到对应记录！",'remark':s_})
        except Exception as e:
            message['msg'] = str(e)
            log.error(message)
            return message
    return message


# MYSQL 拼接时用的时候处理 不处理kv
def cmmQueryMysql(s_db:str,s_project:str,s_sql:str,sqlid:str,i_page_num=1,i_page_size=1000)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'fun cmmQueryMysql'
    message['info']['sqlid'] = sqlid
    log.debug(f">>> {message['info']['fun']} 执行语句 :\n{s_sql}")

    i_total = 1
    s_total_sql = f"select count(*) AS total from ({s_sql}) t1"
    with engine(s_db,s_project).connect() as conn:
        if i_page_size > 1 and i_page_num == 1:
            try:
                res = conn.exec_driver_sql(s_total_sql)
                i_total = res.fetchone()[0]
            except Exception as e:
                message.update({'msg':str(e)})
                log.error(message,'s_total_sql')
                return message
            if i_total == 0:
                message.update({'data':{'fields':[],'datalist':[],'total':0,'pageNum':i_page_num,'pageSize':i_page_size},'code':200,'msg':"No Data"})
                return message
            elif i_total > i_page_size:
                s_sql = f"{s_sql} LIMIT {(i_page_num-1) * i_page_size},{i_page_size}"

        try:
            res = conn.exec_driver_sql(s_sql)
            i_rc = res.rowcount
            l_ds = res.fetchall()
            l_field = list(res.keys())
            message.update({'data':{'datalist':l_ds,'fields':l_field,'total':i_total,'pageNum':i_page_num,'pageSize':i_page_size},'code':200,'msg':"SUCESS"})   
        except Exception as e:
            message.update({'remark':s_sql.replace('\r\n',' '),'msg':str(e)})
            log.error(message,'s_sql')
            return message
        log.debug(f"<<< {message['info']['fun']} 命中数：{i_rc}")
    return message


# MYSQL 执行 拼接时用的时候处理 不处理kv
def cmmExecMysql(s_db:str,s_project:str,s_sql:str,sqlid:str)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'fun cmmExecMysql'
    message['sqlid'] = sqlid
    log.debug(f">>> {message['info']['fun']} 执行语句 :{s_sql}")

    with engine(s_db,s_project).connect() as conn:
        try:
            res = conn.exec_driver_sql(s_sql)
            i_rc = res.rowcount
            conn.commit()
            message.update({'code':200,"count":i_rc,'msg':f"> 更新数：{i_rc}"})   
        except Exception as e:
            message.update({'remark':s_sql.replace('\r\n',' '),'msg':str(e)})
            log.error(message)
            return message
    log.debug(f"<<< {message['info']['fun']} 更新数：{i_rc}")
    return message


# 查询单号信息
def billInfo(s_billid: str)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'billInfo'

    if len(s_billid) != 15:
        message.update({'msg':f"billid {s_billid} 长度 不合规"})
        return message
    j_bill_key = reverse_dict(GLOBAL['BILL_KEY'])
    s_hdr = j_bill_key.get(int(s_billid[0:3]),'').lower()
    log.debug(s_hdr,'s_hdr')
    if not s_hdr:
        message.update({'msg':f"billid {s_billid} 未注册的单据类型"})
        return message
    s_project = s_hdr.split('_')[0].upper()
    log.debug(s_project,'s_project')
    if s_project not in DB_LINK:
        message.update({'msg':f"billid {s_billid} 单据项目未配置连接参数"})
        return message
    
    s_sql = f"SELECT * FROM {s_hdr} WHERE billid = {s_billid};"
    j_ = cmmQueryMysql(s_project.lower(),s_project,s_sql,'billInfo',i_page_num=1,i_page_size=1)
    j_.update({'s_project':s_project,'s_hdr':s_hdr})
    return j_


# 查询单号信息
def billDel(s_billid: str)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'billDel'

    j_ = l2d(billInfo(s_billid))
    log.debug(j_,'billInfo message')
    if j_['code'] > 200:
        return j_
    if j_['data'].get('total',0) ==0:
        message.update({'code':201,'msg':f'未查询到单据 {s_billid}'})
        return j_
    else:
        blsid = j_['data']['datalist'][0].get('blsid',-99)
        s_project = j_['s_project']
        s_hdr = j_['s_hdr']
        s_dtl = s_hdr[:-3] + "dtl"
    if blsid not in (0,1):
        message.update({'msg':f'当前单据【{s_billid}】状态为【{blsid}】不允许删除！'})
        return message
    
    s_sql = f"DELETE FROM {s_hdr} WHERE billid = {s_billid};"
    j_ = cmmExecMysql(s_project.lower(),s_project,s_sql,'billDel')
    s_sql = f"DELETE FROM {s_dtl} WHERE billid = {s_billid};"
    j_ = cmmExecMysql(s_project.lower(),s_project,s_sql,'billDel')
    return j_


# 单号生成
def billId(s_bill_key: str,bltid:int)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'billid'

    i_bill_key = GLOBAL['BILL_KEY'].get(s_bill_key.upper(),-99)
    s_weekday = str(pd.Timestamp.now().weekday() +1)
    kkktyymmdd = f"{str(i_bill_key)}{str(bltid)}{pd.Timestamp.now().strftime('%y%m%d')}"
    try:
        if rs.exists(kkktyymmdd):
            rs.incr(kkktyymmdd,1)
            s_4 = f"0000{rs.get(kkktyymmdd)}"[-4:]
        else:
            rs.set(kkktyymmdd,1)
            rs.expire(kkktyymmdd, 60*60*24)
            s_4 = "0001"
    except Exception as e:
        message['msg'] = str(e)
        log.error(message)
        return message
    s_billid = f"{kkktyymmdd}{s_4}{s_weekday}"
    message.update({'code':200,'billid':s_billid})
    log.debug(s_billid,'billid')
    return message


# MSSQL
def commonQueryMssql(s_db:str,s_project:str,s_sql:str,sqlid:str)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'fun commonQueryMssql'
    message['sqlid'] = sqlid
    log.debug(f">>> {message['info']['fun']} MSSQL {s_project} 执行:{s_sql}")
    i_rc = 0
    # i_total = 0
    # s_total_sql = f"select count(*) AS total from ({s_sql}) t1"
    with engine(s_db,s_project).connect() as conn:

        try:
            res = conn.exec_driver_sql(s_sql)
            # dbcur.execute(s_sql.encode('cp936'))
            l_ds = res.mappings().all()
            i_rc = res.rowcount     #<<
            message.update({'data':{'datalist':l_ds},'code':200,'count':i_rc,'msg':f">>> {message['info']['fun']} 命中数:{i_rc}"})
        except Exception as e:
            message.update({'remark':s_sql.replace('\r\n',' ').replace('\t',' '),'msg':f"{str(e)}"})
            log.error(message)
            return message
    log.debug(f"<<< {message['info']['fun']} MS命中数：{i_rc}")            
    return message


# REDIS 执行 具体功能 明确入参
def cmmRedis(redis_name:str,time_expire=0,fields_list =[],data_list=[],redis_db= 0):
    message = MESSAGE.copy()
    message['info']['fun'] = 'commonJobs_fun cmmRedis'
    log.debug(f">>> {message['info']['fun']} name {redis_name} :{fields_list}")

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
            message.update({'msg':" REDIS STR 未传入 rs_cal"})
            return message            
        rs.set(redis_name,rs_val)
        rs.expire(redis_name,time_expire)
        message.update({'count':1,'code':200,'msg':f"> DB = {redis_db} name = {redis_name} value {rs_val} time_expire={time_expire} 成功"})
        return message
    if redis_name not in fields_list:
        message.update({'msg':f" 关键字段 {redis_name} 在 table_name 中设置 与字段不配 {fields_list}"})
        return message
    
    try:
        _i = fields_list.index(redis_name)
        for ls in data_list:
            key_info =f"{redis_name}:{ls[_i]}"
            _dic = {}
            for i in range(_s):
                if ls[i]:# 需要转换
                    if isinstance(ls[i], datetime):
                        _dic[fields_list[i]] = ls[i].strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(ls[i], date):
                        _dic[fields_list[i]] = ls[i].strftime("%Y-%m-%d")
                    elif isinstance(ls[i], decimal.Decimal):
                        _dic[fields_list[i]] = float(ls[i])
                    else:
                        _dic[fields_list[i]] = ls[i]
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
        message.update({'count':rc,'code':200,'msg':f"> KEY = {redis_name} time_expire={time_expire} rc {rc} 成功"})
        return message
    except Exception as e:
        message.update({'msg':f" REDIS 连接失败  {str(e)}"})
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
    else:
        _b = False
    return _b


# 【角色】TWO 查用户角色 返回一个STR 定制化
def rolesList(userid)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'rolesList'
    log.debug(f">>> {message['info']['fun']} 查用户角色 返回一个去重后的 LIST")

    try:
        df = pd.read_sql_query("""SELECT role_code FROM ct_user2role WHERE userid = %(userid)s group by role_code;"""
            ,engine(),params={'userid':userid}).drop_duplicates()
        i_rc = df.shape[0]
    except Exception as e:
        message.update({'msg':str(e)})
        log.error(message)
        return message
    if i_rc:
        l_ds = df['role_code'].to_list()
        message.update({'code':200,'count':i_rc,'l_role':l_ds})
    else:
        message['msg'] = f"用户 {userid} 未配置角色"
    return message


# 用户登陆 定制化 /auth/v1/login
def login(userid):
    message = MESSAGE.copy()
    message['info']['fun'] = 'login'
    log.debug(f">>> {message['info']['fun']} 用户登陆 ")

    i_rc = 0
    s_sql = "SELECT userid,user_name FROM mdm_user WHERE sid = %s AND userid = %s"

    with engine().connect() as conn:
        try:
            res = conn.exec_driver_sql(s_sql,(SID,userid))
            i_rc = res.rowcount
            if i_rc:
                j_ds = dict(res.mappings().all()[0])
                log.debug(j_ds)
                message.update({'code':200,'count':i_rc,'data':j_ds})
            else:
                message['msg'] = f"未授权用户 {userid}"            
        except Exception as e:
            message.update({'msg':str(e)})
            log.error(message)
        finally:
            return message


def menuIds(l_role:list):
    message = MESSAGE.copy()
    message['info']['fun'] = 'menuIds'
    log.debug(f">>> {message['info']['fun']} MENU THREE 菜单权限  输入一个ROLES 返回 权限IDS ")

    s_sql = """
	SELECT a.menu_code FROM ct_permission2menu a
	INNER JOIN set_permission b ON a.permission_code = b.permission_code
	INNER JOIN ct_permission2role c ON b.permission_code = c.permission_code
	WHERE c.role_code IN %(roles)s
	GROUP BY a.menu_code;"""

    try:
        df = pd.read_sql_query(s_sql,engine(),params={'roles':l_role}).drop_duplicates()
        i_rc = df.shape[0]
    except Exception as e:
        message.update({'msg':str(e)})
        log.error(message)
        return message
    if i_rc:
        l_ds = df['menu_code'].to_list()
        message.update({'code':200,'count':i_rc,'data':l_ds})
    else:
        message.update({'code':200,'count':i_rc,'data':"","msg":f" 角色 {l_role} 未配置 【菜单】权限"})
    return message


# 菜单增加 meta: {icon: "MessageBox", title: "超级表格", isLink: "", isHide: false, isFull: false, isAffix: false, isKeepAlive: true}
def menuListPermission(ids=None):
    message = MESSAGE.copy()
    message['info']['fun'] = 'menuListPermission'
    log.debug(f">>> {message['info']['fun']} 返回MENU菜单权限 ids {ids}")

    l_res = list()

    i_rc = 0
    s1 = "SELECT a.menu_code,a.parent_code,a.menu_name,a.path,a.icon,a.affix,a.full,a.hide,a.keep_alive,a.link,a.redirect,a.component,a.flow_no FROM set_menu a WHERE visible = 1 AND a.parent_code = %s"
    s_sql = f"{s1} AND a.menu_code IN ({ids}) ORDER BY a.flow_no" if ids else f"{s1} ORDER BY a.flow_no"

    with engine().connect() as conn:
        res = conn.exec_driver_sql(s_sql,('root',))
        i_rc = res.rowcount
        l_ds = res.mappings().all()
        if i_rc == 0:
            message['msg']= "业务 无菜单"
            return message

        for row in l_ds:
            j_ = {}
            children = []
            meta = {}
            meta['icon']= row['icon']
            meta['title']= row['menu_name']
            meta['isAffix']= True if row['affix'] else False
            meta['isFull']= True if row['full'] else False
            meta['isHide']= True if row['hide'] else False
            meta['isKeepAlive']= True if row['keep_alive'] else False
            meta['isLink']= row['link']
            j_['meta'] = meta
            j_['name'] = row['menu_code']
            j_['path'] = row['path']
            j_['redirect'] = row['redirect']
            j_['component'] = row['component']
            j_['flow_no'] = row['flow_no']

            res =conn.exec_driver_sql(s_sql,(row['menu_code'],))
            l_ds1 = res.mappings().all()
            i_rc += res.rowcount     #<<
            if l_ds1:
                for row1 in l_ds1:
                    dic1 = {}
                    meta1 = {}
                    meta1['icon']= row1['icon']
                    meta1['title']= row1['menu_name']
                    meta1['isAffix']= True if row1['affix'] else False
                    meta1['isFull']= True if row1['full'] else False
                    meta1['isHide']= True if row1['hide'] else False
                    meta1['isKeepAlive']= True if row1['keep_alive'] else False
                    meta1['isLink']= row1['link']
                    dic1['name'] = row1['menu_code']
                    dic1['path'] = row1['path']
                    dic1['redirect'] = row1['redirect']
                    dic1['component'] = row1['component']
                    dic1['flow_no'] = row1['flow_no']
                    dic1['meta'] = meta1
                    children.append(dic1)
                j_['children'] = children
            l_res.append(j_) 
    message.update({'code':200,'count':i_rc,'data':l_res})
    return message


# 【按钮】 之前的dict 变成list
def buttonPermission(roles:str)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'buttonPermission'
    log.debug(f">>> {message['info']['fun']} 返回页面按钮权限 ")

    s_sql = """SELECT d.menu_code,a.button_code FROM ct_permission2button a
	INNER JOIN set_permission b ON a.permission_code = b.permission_code
	INNER JOIN set_menu d ON a.menu_code = d.menu_code
	INNER JOIN ct_permission2role c ON b.permission_code = c.permission_code"""
    s_sql = f"{s_sql} WHERE c.role_code IN ({roles})" if roles else s_sql
    s_sql += " GROUP BY d.menu_code,a.button_code;"

    with engine().connect() as conn:
        res = conn.exec_driver_sql(s_sql)
        l_ds = res.mappings().all()
        i_rc = res.rowcount
        j_ = dict()

        for row in l_ds:
            j_.update({row['menu_code']:[]})
        for row in l_ds:
            j_[row['menu_code']].append(row['button_code'])
        message.update({'code':200,'count':i_rc,'data':j_})
    return message


# 获取Bearer
def getBearer()->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'getBearer'
    log.debug(f">>> {message['info']['fun']}")

    if rs.exists('job_bearer'):
        s_bearer = rs.get('job_bearer')
        log.debug(s_bearer,'rs_bearer')
        message.update({'code':200,'data':s_bearer})
    else:
        HEADERS = {'Content-Type':'application/json'}
        URL = f"http://{PF_LINK['DH']['HOST']}:{PF_LINK['DH']['PORT']}/api/auth/login"
        JSON = {"username":PF_LINK['DH']['USER'],"password":PF_LINK['DH']['PWD'],"rememberMe":1}
        res = requests.post(URL, json=JSON, headers = HEADERS)
        j_res = json.loads(res.content)
        if j_res['code'] >200:
            message.update({'msg':j_res['content']})
            log.error(message,j_res['code'])
        elif 'content' not in j_res:
            message.update({'msg':'返回 no content'})
            log.error(message)
        elif 'data' not in j_res['content']:
            message.update({'msg':'返回 no data'})
            log.error(message)
        else:
            s_bearer = j_res['content']['data']
            log.debug(s_bearer,'xxl_bearer')
            j_ = cmmRedis('job_bearer',data_list=[s_bearer],time_expire=8*60*60)
            if j_['code']>200:
                return j_
            if rs.exists('job_bearer'):
                s_bearer = rs.get('job_bearer')
            message.update({'code':200,'data':s_bearer})
    return message


# 推送JOB任务
def postJob(jobid:int,j_args={})->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'postJob'
    log.debug(f">>> {message['info']['fun']}")

    j_ = getBearer()
    if j_['code']>200:
        return j_
    else:
        s_bearer = j_['data']
    
    HEADERS = {'Content-Type':'application/json','Authorization':s_bearer}
    URL = f"http://{PF_LINK['DH']['HOST']}:{PF_LINK['DH']['PORT']}/api/job/trigger"
    JSON = {"jobId":jobid,"executorParam":str(j_args)}
    log.debug(HEADERS)

    res = requests.post(URL, json=JSON, headers = HEADERS)
    j_res = json.loads(res.content)
    message.update(j_res)
    if j_res['code'] !=200:
        log.error(message)
    return message