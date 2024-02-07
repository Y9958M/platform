# -*- coding:utf-8 -*-
from main import MESSAGE, SID, GLOBAL, engine, HandleLog

log = HandleLog(__name__)

# 校验手机号码
def checkPhone(phone):
    message = MESSAGE.copy()
    message['fun'] = 'checkPhone'
    log.debug(f">>> {message['fun']} 检查通用查询的入参 \n{phone}  ")
    s_phone = str(phone)
    if len(s_phone) == 11 and s_phone[0:1] == '1':
        message.update({'code':200})
    else:
        message.update({'msg':f"请输入正确的手机号 {s_phone}"})
    return message


def tuple2Str(tuple_):
    s1 = ""
    for s in tuple_:
        s1 += f",'{s[0]}'"
    return s1[1:]


# 【角色】TWO 查用户角色 返回一个STR 定制化
def rolesStr(userid):
    message = MESSAGE.copy()
    message['fun'] = 'rolesStr'
    log.debug(f">>> {message['fun']} 查用户角色 返回一个STR ")

    i_rc = 0
    s_sql = f"""SELECT role_code FROM ct_user2role WHERE userid ={userid}"""
    with engine().connect() as conn:
        try:
            res = conn.exec_driver_sql(s_sql)
            i_rc = res.rowcount
        except Exception as e:
            message.update({'msg':str(e)})
            log.error(message)
            return message
    if i_rc:
        message.update({'code':200,'count':i_rc,'data':tuple2Str(res.fetchall())})
    else:
        message['msg'] = f"用户 {userid} 未配置角色"
    return message


# 用户登陆 定制化 /auth/v1/login
def login(userid):
    message = MESSAGE.copy()
    message['fun'] = 'login'
    log.debug(f">>> {message['fun']} 用户登陆 ")

    i_rc = 0
    s_sql = f"SELECT userid,user_name FROM mdm_user WHERE sid = %s AND userid = %s"

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
            return message

    return message


def menuIds(roles:str):
    message = MESSAGE.copy()
    message['fun'] = 'menuIds'
    log.debug(f">>> {message['fun']} MENU THREE 菜单权限  输入一个ROLES 返回 权限IDS ")

    i_rc = 0
    s_sql = f"""
	SELECT a.menu_code FROM ct_permission2menu a
	INNER JOIN set_permission b ON a.permission_code = b.permission_code
	INNER JOIN ct_permission2role c ON b.permission_code = c.permission_code
	WHERE c.role_code IN ({roles})
	GROUP BY a.menu_code"""

    with engine().connect() as conn:
        try:
            res = conn.exec_driver_sql(s_sql)
            i_rc = res.rowcount
        except Exception as e:
            message.update({'msg':str(e)})
            log.error(message)
            return message
    if i_rc:
        message.update({'code':200,'count':i_rc,'data':tuple2Str(res.fetchall())})
    else:
        message.update({'code':200,'count':i_rc,'data':"","msg":f" 角色 {roles} 未配置 【菜单】权限"})
    return message


# 菜单增加 meta: {icon: "MessageBox", title: "超级表格", isLink: "", isHide: false, isFull: false, isAffix: false, isKeepAlive: true}
def menuListPermission(ids=None):
    message = MESSAGE.copy()
    message['fun'] = 'menuListPermission'
    log.debug(f">>> {message['fun']} 返回MENU菜单权限 ids {ids}")

    l_res = list()

    i_rc = 0
    s1 = f"SELECT a.menu_code,a.parent_code,a.menu_name,a.path,a.icon,a.affix,a.full,a.hide,a.keep_alive,a.link,a.redirect,a.component,a.flow_no FROM set_menu a WHERE visible = 1 AND a.parent_code = %s"
    s_sql = f"{s1} AND a.menu_code IN ({ids}) ORDER BY a.flow_no" if ids else f"{s1} ORDER BY a.flow_no"

    with engine().connect() as conn:
        res = conn.exec_driver_sql(s_sql,('root',))
        i_rc = res.rowcount
        l_ds = res.mappings().all()
        if i_rc == 0:
            message['msg']= f"业务 无菜单"
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
    message['fun'] = 'buttonPermission'
    log.debug(f">>> {message['fun']} 返回页面按钮权限 ")

    s_sql = f"""SELECT d.menu_code,a.button_code FROM ct_permission2button a
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