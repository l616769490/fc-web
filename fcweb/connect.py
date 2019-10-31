import json
import redis
import pymysql
import fcutils
from .sign import DBSign, RedisSign
from fcutils import getConfig

@DBSign
def getDB():
    """ 获取数据库连接
    --
    """
    pass

@RedisSign
def getRedis():
    """ 获取redis连接
    --
    """
    pass

def guideCode2Session(code):
    ''' 导游端获取sessionkey和openid(unionid)
    --
        @return 
            {
                "session_key": "oEB5VKcfmuVTWDVccERB\/w==",
                "openid": "oVcrr1ZmN5MbcLS-16ApTyJUb_zg",
                "unionid":"sadasfsdfsdfsrehbf"
            }
    '''
    return _getCode2Session(code, WX_GUIDE_FILE_NAME)

def userCode2Session(code):
    ''' 游客端获取sessionkey和openid(unionid)
    --
        @return 
            {
                "session_key": "oEB5VKcfmuVTWDVccERB\/w==",
                "openid": "oVcrr1ZmN5MbcLS-16ApTyJUb_zg",
                "unionid":"sadasfsdfsdfsrehbf"
            }
    '''
    return _getCode2Session(code, WX_USER_FILE_NAME)

def _getCode2Session(code, confName):
    ''' 获取sessionkey和openid(unionid)
    --
        @return 
            {
                "session_key": "oEB5VKcfmuVTWDVccERB\/w==",
                "openid": "oVcrr1ZmN5MbcLS-16ApTyJUb_zg",
                "unionid":"sadasfsdfsdfsrehbf"
            }
    '''
    # 读取配置文件
    conf = json.loads(fcutils.getDataForStr(CONF_HOST, confName).text)
    if conf['status'] != '200':
        return None
    confData = json.loads(conf['data'])
    appid = confData['appid']
    secret = confData['secret']
    code2session_host = CODE2SESSION_HOST % (appid, secret, code)

    code2Session = fcutils.getData(code2session_host).text
    return json.loads(code2Session)