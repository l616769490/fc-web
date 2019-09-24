#####################################################################
#
# 工具文件
#
#####################################################################
import re
import json
import time
from .response import ResponseEntity

def responseFormat(responseEntitys, start_response, token = None):
    ''' 格式化返回数据
    :param res 返回数据
    :param start_response 函数计算的start_response
    :param token 用户token
    :return 按照函数计算的格式返回数据
    '''
    if not isinstance(responseEntitys, ResponseEntity):
        raise TypeError('只支持ResponseEntity格式的返回值')
    
    res = responseEntitys.build(start_response, token)
    codeRes = dataToJson(res)
    return [json.dumps(codeRes).encode()]

def dataToJson(data):
    ''' 把list和dict转换成json字符串,
        json库无法转换的类型（Decimal和日期类型）会转化为字符串形式, 
        传入其他类型的数据转化成string返回
    '''
    if isinstance(data, str):
        if data.startswith('{') and data.endswith('}') or data.startswith('[') and data.endswith(']'):
            return json.loads(data.replace("'", '"'))
        return data
    elif isinstance(data, list):
        for item in data:
            item = dataToJson(item)
        return data
    elif isinstance(data, dict):
        for k, v in data.items():
            data[k] = dataToJson(v)
        return data
    else:
        return str(data)

def pathMatch(path, pattern = None):
    ''' 解析路径
    :params path 路径，路径中形如【xxxx?key=value&key=value】的字符串会被解析成键值对
    :params pattern 路径模板。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段
                    会将path中对应位置的路径解析为key的值        
    '''
    params = {}
    n = path.rfind('?')
    # 获取?后面的参数
    if n != -1:
        paths = path[n + 1:]
        if len(paths) > 0:
            arr = paths.split('&')
            for a in arr:
                aa = a.split('=')
                if len(aa) == 2:
                    params[aa[0]] = _format(aa[1])
    # 获取模板中的参数
    if pattern:
        paths1 = pattern.split('/')
        paths2 = path.split('/') if n == -1 else path[:n].split('/')
        if len(paths2) == len(paths1):
            for i, a in enumerate(paths1):
                if a.startswith('{') and a.endswith('}'):
                    key = a[1:-1]
                    if len(key) > 0:
                        if key not in params:
                            params[key] = _format(paths2[i])
    return params

def _format(s):
    ''' 把传入的字符串格式化成对应的格式：字符串；数字；json
    '''
    if not s or len(s) == 0:
        return ''
    
    if s.startswith('{') and s.endswith('}') or s.startswith('[') and s.endswith(']'):
        return json.loads(s)
    
    if s.isdigit():
        if s.startswith('0'):
            return s
        else:
            return int(s)
    
    if s.startswith('-') and s[1:].isdigit():
        return int(s)
    
    try:
        f = float(s)
        return f
    except ValueError:
        return s

def createId(environ):
    ''' 生成ID
    '''
    now = int(time.time())
    start = int(time.mktime(time.strptime('2019-08-01 00:00:00', "%Y-%m-%d %H:%M:%S")))
    temp = str(now - start)
    if len(temp) < 15:
        temp = ("0" * (15-len(temp))) + temp 

    serviceName = str(int('0x' + environ['SERVER_NAME'], 16))
    if len(serviceName) < 15:
        serviceName = ("0" * (15 - len(serviceName))) + serviceName
    if len(serviceName) > 15:
        serviceName = serviceName[:15]

    return temp+serviceName