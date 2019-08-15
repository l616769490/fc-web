#####################################################################
#
# 工具文件
#
#####################################################################
import re
import json
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
    
    return responseEntitys.build(start_response, token)



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
                        params[key] = _format(paths2[i])
    return params

def _format(str):
    ''' 把传入的字符串格式化成对应的格式：字符串；数字；json
    '''
    if not str or len(str) == 0:
        return ''
    
    if str.startswith('{') and str.endswith('}') or str.startswith('[') and str.endswith(']'):
        return json.loads(str)
    
    if str.isdigit():
        return int(str)
    
    if str.startswith('-') and str[1:].isdigit():
        return int(str)
    
    try:
        f = float(str)
        return f
    except ValueError:
        return str

if __name__ == "__main__":

    res = ResponseEntity('200')
    responseFormat('res')


