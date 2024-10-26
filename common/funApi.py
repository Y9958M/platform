# -*- coding:utf-8 -*-
import requests
import pickle
import os
from cmm import MESSAGE,API_LINK,HandleLog,rs,json
from .fun import cmmRedis

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-08-30
# description: API相关操作 明确传入的值
s_url_dd = API_LINK['DD']['URL']
appkey_dd = API_LINK['DD']['APPKEY']
appsecret_dd = API_LINK['DD']['SECRET']

# 获取钉钉的token 存入redis
def getAccessToken()->dict:
    url = f"{s_url_dd}/gettoken?appkey={appkey_dd}&appsecret={appsecret_dd}"
    message = MESSAGE.copy()
    message['info']['fun'] = 'getAccessToken'
    log.debug(f">>> {message['info']['fun']}")

    if rs.exists('access_token_dd'):
        access_token = rs.get('access_token_dd')
        log.debug(access_token,'access_token_dd')
        message.update({'code':200,'access_token':access_token})
        return message
    else:
        try:
            j_res = requests.get(url=url).json()
            log.debug(j_res,'钉钉返回信息')
        except Exception as e:
            message.update({'msg':str(e)})
            log.error(message)
            log.error(url)

        message.update(j_res)
        if j_res.get('errcode',-99) == 0:
            access_token = j_res.get('access_token')
            j_ = cmmRedis('access_token_dd',data_list=[access_token],time_expire=j_res.get('expires_in',60))
            if j_['code']>200:
                log.debug(j_)
                return j_
            if rs.exists('access_token_dd'):
                access_token = rs.get('access_token_dd')
                log.debug(access_token,'access_token_dd 2')
                message.update({'code':200,'access_token':access_token})

        log.debug(url)
    return message

# 获取钉钉的用户信息
def getDdUser(access_token,params)->dict:
    url = f"{s_url_dd}/topapi/v2/user/get?access_token={access_token}"
    message = MESSAGE.copy()
    message['info']['fun'] = 'getDdUser'
    log.debug(f">>> {message['info']['fun']} params:{params}")

    try:
        j_res = requests.get(url=url,params=params).json()

    except Exception as e:
        message.update({'msg':str(e)})
        log.error(message)
        log.error(url)

    message.update(j_res)
    if j_res.get('errcode',-99) == 0:
        message.update({'code':200})
    log.debug(url)
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
        URL = f"http://{API_LINK['DH']['HOST']}:{API_LINK['DH']['PORT']}/api/auth/login"
        JSON = {"username":API_LINK['DH']['USER'],"password":API_LINK['DH']['PWD'],"rememberMe":1}
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


# 获取 Cookie
def getCookie()->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'getCookie'
    data={'userName':API_LINK['XXL']['USR'],'password':API_LINK['XXL']['PWD'],}
    log.debug(f">>> {message['info']['fun']} {data}")
    # 发送 POST 请求进行登录
    login_url = f"{API_LINK['XXL']['URL']}/login"
    log.debug(login_url,'login_url')
    response = requests.post(login_url, data=data)

    message['code'] = response.status_code
    res = json.loads(response.text)
    log.debug(type(res),'res')
    log.debug(res)
    if message['code'] > 200:
        return message
    else:
        message['msg'] = res
        log.debug(type(message['msg']))
        log.debug(message['msg'])
        message['code'] =   res.get('code',200)
        message['remark'] = res.get('content','')
        message['msg'] =    res.get('msg','')
    if message['code'] > 200:
        return message
    # 保存 Cookie
    with open('cookie.pkl', 'wb') as f:
        pickle.dump(response.cookies, f)

    return message

# 推送JOB任务
def postJob(j_args={})->dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'postJob'
    url = f"{API_LINK['XXL']['URL']}/jobinfo/trigger"
    log.debug(f">>> {message['info']['fun']}, {url}")

    file_path = 'cookie.pkl'
    if(not os.path.isfile(file_path)):
        j_ = getCookie()
        if j_['code'] > 200:
            message.update(j_)
            return message
        
    # 下次使用 Cookie
    with open('cookie.pkl', 'rb') as f:
        cookies = pickle.load(f)
    # 使用保存的 Cookies 进行后续访问
    response = requests.post(url, cookies=cookies,data=j_args)
    message['code'] = response.status_code
    res = json.loads(response.text)
    message['msg'] = res
    if message['code'] > 200:
        return message
    else:
        message['code'] =   res.get('code',200)
        message['remark'] = res.get('content','')
        message['msg'] =    res.get('msg','')
    return message

# 推送JOB任务
# def postJob(j_args={})->dict:
#     message = MESSAGE.copy()
#     message['info']['fun'] = 'postJob'
#     log.debug(f">>> {message['info']['fun']}")

#     j_ = getBearer()
#     if j_['code']>200:
#         return j_
#     else:
#         s_bearer = j_['data']
    
#     HEADERS = {'Content-Type':'application/json','Authorization':s_bearer}
#     URL = f"http://{API_LINK['DH']['HOST']}:{API_LINK['DH']['PORT']}/api/job/trigger"
#     JSON = {"jobId":jobid,"executorParam":str(j_args)}
#     log.debug(HEADERS)

#     res = requests.post(URL, json=JSON, headers = HEADERS)
#     j_res = json.loads(res.content)
#     message.update(j_res)
#     if j_res['code'] !=200:
#         log.error(message)
#     return message

