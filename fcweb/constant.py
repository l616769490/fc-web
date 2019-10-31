import json
# 配置文件参数名
CONF_CENTER_NAME = 'conf_center'

# mysql配置文件名字
SQL_CONF_FILE_NAME = 'sql'

# redis配置文件名
REDIS_CONF_FILE_NAME = 'redis'

# 导游微信配置文件名
WX_GUIDE_FILE_NAME = 'wx_guide'

# 游客微信配置文件名
WX_USER_FILE_NAME = 'wx'

# 公钥
RSA_PUBLIC_KEY_FILE_NAME = 'rsa_public_key'
# 密钥
RSA_PRIVATE_KEY_FILE_NAME = 'rsa_private_key'

# 微信open Id请求地址
CODE2SESSION_HOST = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'

from fcutils import getConfig, getConfigFromConfCenter

_dict = {}

def getConfByName(confName):
    ''' 获取配置
    ''' 
    global _dict
    if confName in _dict:
        return _dict[confName]
    elif CONF_CENTER_NAME in _dict:
        conf_center = _dict[CONF_CENTER_NAME]
        res = getConfigFromConfCenter(conf_center['url'], confName, conf_center['pwd'] )
        if res.status_code != 200:
            raise Exception('从配置中心获取密钥失败！')
        data = res.text
        try:
            data = json.loads(data)
        except Exception as e:
            data = str(data)
        _dict[confName] = data
        return data
    else:
        raise Exception('')

def initConfCenter(environ):
    ''' 获取配置中心url和pwd
    '''
    global _dict
    try:
        conf_center = getConfig(CONF_CENTER_NAME)
        if not conf_center:
            raise Exception('配置中心的url和pwd必须配置')

        if not conf_center['url'].startswith('http'):
            httpHost = environ['HTTP_HOST'] if 'HTTP_HOST' in environ else environ['REMOTE_ADDR']
            conf_center['url'] = 'https://{}/2016-08-15/proxy/{}/'.format(httpHost, conf_center['url'])
        
        _dict[CONF_CENTER_NAME] = conf_center
    except Exception as e:
        raise Exception('请在application.py中配置配置中心url和pwd')