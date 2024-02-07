# -*- coding:utf-8 -*-
from main import HandleLog,MESSAGE,ADMIN

from .fun import login, buttonPermission, menuIds, rolesStr, menuListPermission,checkPhone, tuple2Str

log = HandleLog('auth-foo')

# author  :don
# date    :2022-05-30
# description: 提供内部标准功能 组装模块 可实现对应完整功能 


# 用户登录
def authLoginMain(userid):
    message = MESSAGE.copy()
    message['fun'] = 'authLoginMain'
    log.debug(f">>> {message['fun']} 查手机号 isUserExist {userid}")
    j_ = dict()

    j_ = checkPhone(userid)
    if j_['code'] > 200:
        return j_

    return login(userid)


# 【菜单】权限 
def authMenuListMain(userid):
    message = MESSAGE.copy()
    message['fun'] = 'authMenuListMain'
    log.debug(f">>> {message['fun']} 菜单相关权限 {userid} ")
    j_ = dict()

    log.debug(f"ONE 【菜单】先查 用户 USER_NO 是否管理员")

    if int(userid) in ADMIN:
        log.warning(f"管理员 【菜单】权限 {userid} ")
        return menuListPermission()

    log.debug("TWO 【菜单】通用 用户 角色关系表 查出用户的所有角色 ")
    j_.clear()
    j_ = rolesStr(userid)
    if j_['code'] > 200:return j_
    else:
        roles = j_['data']

    log.debug("THREE 【菜单】[定制] 角色下所有的 菜单相关权限 ")
    j_.clear()
    j_ = menuIds(roles)
    if j_['code'] > 200:return j_
    else:
        ids = j_['data']
        log.debug(ids)
    log.debug("FOUR 【菜单】 返回结果 定制")
    return menuListPermission(ids)  


# 【按钮】权限
def authUserButtonMain(userid):
    message = MESSAGE.copy()
    message['fun'] = 'authUserButtonMain'
    log.debug(f">>> {message['fun']} BUTTON 按钮相关权限 {userid}")

    log.debug(f"ONE 【按钮】 先查 用户 USER_NO 是否管理员")
    if int(userid) in ADMIN:
        log.warning(f"管理员 【按钮】权限 {userid}")
        return buttonPermission('')

    log.debug(f"TWO 【按钮】通用 用户 {userid} 角色关系表 查出用户的所有角色 ")
    j_ = dict()
    j_ = rolesStr(userid)
    if j_['code'] > 200:return j_
    else:
        roles = j_['data']
    # log.debug(f"THREE 【按钮】[定制] 角色 {roles} 下所有的 ")
    # 如果没有配置权限 返回空
    if userid:
        return buttonPermission(roles)
        # log.debug(f"FOUR 【按钮】返回结果 定制 {ids}")
    else:
        return {'code':200,'count':rc,'data':"","msg":f" 角色 {roles} 未配置【按钮】 权限"}
