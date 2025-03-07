
from cmm import MESSAGE,ADMIN,SID,HandleLog
from .fun import (cmmFetchone,checkSqlContext,ckDbLink,sqlContextToList,swapContent
                  ,cmmQueryMysql,commonQueryMssql,cmmRedis
                  ,checkPhone,rolesList,menuIds,login,menuListPermission,buttonPermission
                  ,billId,billInfo,billDel
                  ,checkDdUser,ddButtonList)
from .funApi import getAccessToken,getDdUser,postJob
from .funSet import setDdUser,getPermissionBraid

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2022-09-23
# description: 组装好模块 调用fun中的数据和utils中的逻辑
# 通用查询中 表和SQLID对应 是否有更好的方法 


# 通用查询 no KV
def commonQueryMain(j_args)->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'foo commonQueryMain'
    log.debug(f">> {message['info']['fun']} 通用查询 入参 {j_args}")

    # 初始返回信息格式
    message.update({'msg':'通用查询','remark':'','data':{
        'datalist': [],
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
        # message['sqlid'] = sqlid
    
    j_ = dict() # 查询平台库 platform
    j_.update(cmmFetchone(sqlid,'common_query'))
    if j_['code'] > 200:
        return j_
    else:
        sql_context =   j_['sql_context']
        s_project   =   j_['project']
        message['info']['sql_name'] = j_['sql_name']
        message['remark']   = j_['remark']
    j_.clear()  # check sql_context 防注入检查'
    j_.update(checkSqlContext(sql_context))

    j_.clear()  # 检查 DB_LINK 连接
    j_.update(ckDbLink(s_project))
    if  j_['code'] >200:
        return j_
    else:
        j_db_info = j_['data']

    try:
        j_.clear()  # 处理 sql_context
        j_.update(sqlContextToList(sql_context))
        if  j_['code'] >200:
            return j_
        else:
            l_sql = j_['data']
    except Exception as e:
        message.update({'msg':str(e),'sql':sql_context})
        log.error(sql_context)
        return message

    j_.clear()  # 查询拼装
    j_.update(swapContent(l_sql,j_args))
    if  j_['code'] >200:
        return j_
    else:
        s_sql = j_['data']

    if   j_db_info['TYPE'] == 'MYSQL':
        message.update(cmmQueryMysql(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid,i_page_num,i_page_size)) 
    elif j_db_info['TYPE'] == 'MSSQL':
        message.update(commonQueryMssql(j_db_info['DB'],j_db_info['PROJECT'],s_sql,sqlid))    # 暂时不支持分页
    else:
        message.update({'msg':f"查询失败 未匹配TYPE: {j_db_info['TYPE']}"})
    return message


# 通用缓存数据(存 入参 KEY {字典} 过期时间)
def commonRedisMain(j_args:dict):
    message = MESSAGE.copy()
    message['info']['fun'] = 'foo commonIntoRedis'
    log.debug(f">> {message['info']['fun']} 通用缓存数据(存 入参 KEY 字典 过期时间) \n{j_args}")
    # 检查入参
    j_ = dict()
    if 'rs_name' not in j_args:
        message.update({'msg':'need rs_name 0'})
        return message
    else:
        # project_name=   j_args['project_name'] if 'project_name' in j_args else 'REDIS'
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
            message.update({'msg':"未传入sqlid"})
            return message
        j_ds = {}
        j_ds = commonQueryMain(j_args)
        if j_ds['code'] > 200:
            return j_ds
        else:
            data_list = j_ds['data']
            fields_list = j_ds['fields_list']

        j_.clear()
        j_ = cmmRedis(redis_name = rs_name,time_expire= time_expire, fields_list= fields_list, data_list= data_list,redis_db= redis_db)
        if j_['code'] > 200:
            return j_
        else:
            message.update({'code':200,'msg':f"成功更新 缓存库 {redis_db} {rs_name}:XXX  过期时间：{time_expire} 秒",'count':j_['count']})
            return message

    elif redis_type in ['HASH']:
        log.debug(f"HASH rs_key {rs_key} rs_val {rs_val}")
        if rs_val and rs_key:
            j_.clear()
            j_ = cmmRedis(redis_name = rs_name,time_expire= time_expire, fields_list= [rs_key], data_list= [rs_val],redis_db= redis_db)
            if j_['code'] > 200:
                return j_
            else:
                message.update({'code':200,'msg':f"成功更新 缓存库 {redis_db} {rs_name},{rs_key},{rs_val}  过期时间：{time_expire} 秒",'count':1})    
        else:
            message.update({'code':201,'msg':f"缺少参数 rs_key {rs_key} rs_val {rs_val}"})
        return message

    elif redis_type in ['STR']:
        log.debug(f"STR rs_val {rs_val}")
        if rs_val:
            j_.clear()
            j_ = cmmRedis(redis_name = rs_name,time_expire= time_expire, fields_list= [], data_list= [rs_val],redis_db= redis_db)
            if j_['code'] > 200:
                return j_
            else:
                message.update({'code':200,'msg':f"成功更新 缓存库 {redis_db} {rs_name}:{rs_val}  过期时间：{time_expire} 秒",'count':1})     
        else:
            message.update({'code':201,'msg':f"缺少参数 rs_val {rs_val}"})
        return message          

    else:
        message.update({'code':200,'msg':f"传入 {redis_type} 不在范围"})
        return message


# 通用单据信息 返回单据所有信息
def cmmBillInfoMain(s_billid:str)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'cmmBillInfoMain'
    log.debug(f">>> {message['info']['fun']} 通用单据信息 {s_billid}")

    return billInfo(str(s_billid))


# 通用删除单据
def cmmBillDelMain(s_billid:str)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'cmmBillDelMain'
    log.debug(f">>> {message['info']['fun']} 通用删除状态为0或1状态的单据 {s_billid}")

    return billDel(str(s_billid))


# 通用单据号 3K1T6D4F1W
def cmmBillidMain(s_bill_key:str,bltid:1)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'cmmBillidMain'
    log.debug(f">>> {message['info']['fun']} 通用单据号 3K1T6D4F1W {s_bill_key}")

    return billId(s_bill_key,bltid)



# 用户登录
def authLoginMain(j_args):
    message = MESSAGE.copy()
    message['info']['fun'] = 'authLoginMain'
    log.debug(f">>> {message['info']['fun']} 查手机号 isUserExist {j_args}")
    j_ = dict()
    userid = j_args.get('phone_no','')
    if not userid:
        pass

    j_ = checkPhone(userid)
    if j_['code'] > 200:
        return j_

    return login(userid)

# DD用户登录
def ddLoginMain(j_args):
    message = MESSAGE.copy()
    message['info']['fun'] = 'ddLoginMain'
    log.debug(f">>> {message['info']['fun']} 查用户userid {j_args}")
    j_ = dict()
    user_code = j_args.get('user_code','')
    if not user_code:
        log.warning(j_args,'没取得用户 user_code')
        message.update({'msg':'无 user_code ?'})
        return message
    # 检查 dd_user里
    j_ = checkDdUser(user_code)

    if j_['code'] > 300:
        return message
    elif j_['code'] > 200:
        j_ = getAccessToken()
        if j_['code'] > 200:
            return j_
        else:
            j_ = getDdUser(j_.get('access_token',''),{'userid':user_code})
            if j_['code']>200:
                log.warning(j_)
                return j_
            else:
                log.debug(j_,'返回钉钉的员工信息')
                j_ = setDdUser(j_)
                if j_['code']> 200:
                    return j_
                else:
                    userid = j_['userid']
                    log.info(userid,'userid 已取得')
                    return login(userid)
    else:
        return login(j_['userid'])
    
# 管理的门店
def ddGetPermissionBraidMain(j_args):
    message = MESSAGE.copy()
    message['info']['fun'] = 'ddGetPermissionBraidMain'
    log.debug(f">>> {message['info']['fun']} 查部门对应门店权限 {j_args}")
    dept_code = j_args.get('dept_code','')
    return getPermissionBraid(dept_code)


# 【菜单】权限 
def authMenuListMain(userid):
    message = MESSAGE.copy()
    message['info']['fun'] = 'authMenuListMain'
    log.debug(f">>> {message['info']['fun']} 菜单相关权限 {userid} ")
    j_ = dict()

    log.debug("ONE 【菜单】先查 用户 USER_NO 是否管理员")

    if int(userid) in ADMIN:
        log.warning(userid,"管理员 【菜单】")
        return menuListPermission()

    log.debug(userid,"TWO 【菜单】通用 用户 角色关系表 查出用户的所有角色 ")
    j_.clear()
    j_ = rolesList(userid)
    if j_['code'] > 200:
        return j_
    else:
        l_role = j_['l_role']

    log.debug(l_role,"THREE 【菜单】[定制] 角色下所有的 菜单相关权限 ")
    j_.clear()
    j_ = menuIds(l_role)
    if j_['code'] > 200:
        return j_
    else:
        s_ids = str(j_['data'])[1:-1]
    log.debug(s_ids,"FOUR 【菜单】 返回结果 定制")
    return menuListPermission(s_ids)  


# 【按钮】权限
def authUserButtonMain(userid):
    message = MESSAGE.copy()
    message['info']['fun'] = 'authUserButtonMain'
    log.debug(f">>> {message['info']['fun']} ONE 【按钮】先查 用户 userid 是否管理员")

    if int(userid) in ADMIN:
        log.warning(userid,"管理员 【按钮】")
        return buttonPermission('')

    log.debug(userid,"TWO 【按钮】通用 用户 角色关系表 查出用户的所有角色 ")
    j_ = dict()
    j_ = rolesList(userid)
    if j_['code'] > 200:
        return j_
    else:
        s_role = str(j_['l_role'])[1:-1]
        i_rc = j_['count']

    # 如果没有配置权限 返回空
    if i_rc:
        return buttonPermission(s_role)
    else:
        return {'code':200,'count':i_rc,'data':"","msg":f" 用户 {userid} 未配置角色 无【按钮】权限"}

# DD【按钮】权限
def ddGetPermissionButtonMain(j_args):
    message = MESSAGE.copy()
    message['info']['fun'] = 'ddGetPermissionButtonMain'
    log.debug(f">>> {message['info']['fun']} 查人员对应菜单 内容 按钮权限 {j_args}")
    j_ = dict()
    userid = j_args.get('userid',0)
    # log.debug(f"ONE 【菜单】先查 用户 {userid} 是否管理员")
    if int(userid) in ADMIN:
        log.warning(userid,"管理员 【ALL按钮】")
        return ddButtonList()
    
    log.debug(userid,"TWO 【按钮】通用 用户 角色关系表 查出用户的所有角色 ")
    j_ = dict()
    j_ = rolesList(userid)
    if j_['code'] > 200:
        return j_
    else:
        s_role = str(j_['l_role'])[1:-1]
        i_rc = j_['count']
    if i_rc:
        return ddButtonList(s_role)
    else:
        log.debug('如果没有配置权限 返回空')
        return {'code':200,'count':i_rc,'data':"","msg":f" 用户 {userid} 未配置角色 无【按钮】权限"}


# JOB任务推送
def postJobMain(j_args={}):
    message = MESSAGE.copy()
    message['info']['fun'] = 'postJobMain'
    log.debug(f">>> {message['info']['fun']}")
    jobid = j_args.get('jobid',0)
    if jobid > 0:
        args = {'sid':SID,'id':jobid,'executorParam':str(j_args)}
        return postJob(args)
    else:
        message['msg'] = f'{jobid} need jobid'
        return postJob(message)
