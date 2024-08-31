# -*- coding:utf-8 -*-
from .cmm import engine, MESSAGE,HandleLog,SID
from .model import DdUser,MdmUser,DdDept,MdmBra
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-08-30
# description: 更新相关操作
se = Session(engine())

def setDdUser(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'setDdUser'
    log.debug(f">>> {message['info']['fun']}")

    res =  j_args['result']
    user_code = res.get('userid','')
    manager_user_code = res.get('manager_userid','')
    user_name = res.get('name','')
    work_code = res.get('job_number','')
    work_place = res.get('work_place','')
    title = res.get('title','')
    dept_code =res.get('dept_id_list','')
    unionid = res.get('unionid','')
    url_avatar = res.get('avatar','')
    mobile = res.get('mobile','')
    permission_purid = [11,12,13,14,21,22,23,24,31,32,33,34,35,36,37,38,39,40,41,51,52,53,54,55,56]

    if len(mobile) == 0:
        log.warning(res,'未取得电话号码 mobile')
        message.update({'msg':'未取得钉钉信息中的电话号码'})
        return message

    stmt = select(DdUser).where(DdUser.user_code == user_code)
    se_user_dd = se.scalars(stmt).first()
    if se_user_dd:
        log.warning(user_code,'DdUser user_code 存在')
    else:
        si2 = insert(DdUser).values(
            mobile = mobile,
            user_code = user_code,
            manager_user_code = manager_user_code,
            user_name = user_name,
            work_code = work_code,
            work_place = work_place,
            title = title,
            dept_code = dept_code,
            unionid = unionid,
            json = res
            )
        try:
            se.execute(si2)
        except Exception as e:
            log.error(e)

    stmt = select(MdmUser).where(MdmUser.userid == mobile)
    se_user_mdm = se.scalars(stmt).first()
    if se_user_mdm:
        log.warning(mobile,'MdmUser userid 存在')
    else:
        si3 = insert(MdmUser).values(
            userid = mobile,
            user_name = user_name,
            url_avatar = url_avatar,
            gender = '',
            mobile = mobile,
            permission_purid = permission_purid,
            sid = SID
            )
        try:
            se.execute(si3)
        except Exception as e:
            log.error(e)
    se.commit()
    message.update({'code':200,'userid':mobile})
    return message


def getPermissionBraid(dept_code)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'getPermissionBraid'
    log.debug(f">>> {message['info']['fun']} dept_code:{dept_code}")

    stmt = select(DdDept).where(DdDept.deptid == dept_code)
    se_dept = se.scalars(stmt).first()
    
    if se_dept:
        try:
            permission_braid = eval(se_dept.permission_braid)
            stmt = select(MdmBra).where(MdmBra.braid.in_(permission_braid))
            se_bra = se.scalars(stmt)
            l_ = []
            for b in se_bra:
                l_.append({'text':b.bra,'value':b.braid})
            message.update({'code':200,'permission_braid':permission_braid,'select_field_bra':l_})
            log.debug(type(permission_braid))
        except Exception as e:
            log.warning(e,'getPermissionBraid 异常')
            message.update({'code':200,'permission_braid':[],'msg':'getPermissionBraid 异常'})
        return message
    else:
        message.update({'code':200,'permission_braid':[],'msg':f'dd_dept中无 {dept_code}'})
        log.warning(dept_code,'no dept_code')
        return message
    
# def deptInsert(l_res):  # 更新部门
#     l_ = []
#     for j_ in l_res:
#         deptid = j_.get('dept_id',1)
#         l_.append(deptid)
#         stmt = select(DdDept).where(DdDept.dept_id == deptid)
#         se_dept = se.scalars(stmt).first()
#         if se_dept:
#             pass
#         else:
#             si = insert(DdDept).values(
#                 parentid = j_.get('parent_id'),
#                 deptid=j_.get('dept_id'),
#                 dept_name = j_.get('name')
#                 )
#             se.execute(si)
        
#     print(l_)
#     for i in l_:
#         j_res = requests.get(f"{s_url}/topapi/v2/department/listsub?access_token={access_token}&dept_id={i}").json()
#         if j_res['errcode'] == 0:
#             l_res = j_res.get('result',[])
#         else:
#             continue

#         l_ = []
#         for j_ in l_res:
#             deptid = j_.get('dept_id',1)
#             l_.append(deptid)
#             stmt = select(DdDept).where(DdDept.deptid == deptid)
#             se_dept = se.scalars(stmt).first()
#             if se_dept:
#                 pass
#             else:
#                 si = insert(DdDept).values(
#                     parentid = j_.get('parent_id'),
#                     deptid=j_.get('dept_id'),
#                     dept_name = j_.get('name')
#                     )
#                 se.execute(si)

#         for i in l_:
#             j_res = requests.get(f"{s_url}/topapi/v2/department/listsub?access_token={access_token}&dept_id={i}").json()
#             if j_res['errcode'] == 0:
#                 l_res = j_res.get('result',[])
#             else:
#                 continue

#             l_ = []
#             for j_ in l_res:
#                 deptid = j_.get('dept_id',1)
#                 l_.append(deptid)
#                 stmt = select(DdDept).where(DdDept.deptid == deptid)
#                 se_dept = se.scalars(stmt).first()
#                 if se_dept:
#                     pass
#                 else:
#                     si = insert(DdDept).values(
#                         parentid = j_.get('parent_id'),
#                         deptid=j_.get('dept_id'),
#                         dept_name = j_.get('name')
#                         )
#                     se.execute(si)

#     se.commit()

# # deptInsert(l_res)




