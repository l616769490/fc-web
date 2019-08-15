import functools
from .utils import pathMatch, responseFormat
import json
from .response import ResponseEntity
import mengyou


def fcIndex(login = False, auth = False, updateToken = True):
    ''' 
    :param login 是否需要登录，默认False
    :param auth 是否需要鉴权，默认False
    :param updateToken 是否更新token，默认True
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            environ = args[0]
            start_response = args[1]
            res = None
            token = None
            if login:   # 是否需要验证登录
                if not mengyou.isLogin(environ):
                    res = ResponseEntity.unauthorized('用户未登录，或登录已过期')
            if auth:    # 是否需要验证权限
                if not mengyou.authRight(environ):
                    res = ResponseEntity.unauthorized('权限不足')
            if updateToken: # 是否需要更新token
                oldToken = mengyou.getTokenFromHeader(environ)
                token = mengyou.updateToken(oldToken)
            
            if not res: # 登录验证和权限验证都通过了，则执行对应的方法
                res = _run(*args, **kw)
            return responseFormat(res, start_response, token)
        return wrapper
    return decorator

def _run(*args, **kw):
    ''' 根据请求类型（GET，POST）执行对应的方法
    '''
    environ = args[0]
    request_method = environ['REQUEST_METHOD']

    # 获取方法列表
    funcs = _getFuncs(environ)
    
    if request_method in funcs:
        # 选择方法
        fn = funcs[request_method]
        return fn(*args, **kw)
    else:
        return '请求类型不支持！'

def get(pattern):
    '''
    :param pattern  路径模板，以/开头，需要带上服务名和函数名。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                    示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                        pattern = '/demo/getUserById/{id}'
                        解析后会自动填充参数id=1
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            # 获取接口地址
            environ = args[0]
            requestUri = environ['fc.request_uri']
            fcInterfaceURL = requestUri.split('proxy')[1].replace('.LATEST', '')
            # 解析参数
            params = pathMatch(fcInterfaceURL, pattern)
            if func.__code__.co_argcount == len(params):
                res = func(**params)
            else:
                res = func(params)
            return res
        wrapper.__method__ = 'GET'
        return wrapper
    return decorator

def _getFuncs(environ):
    ''' 获取方法列表
    :param environ 函数计算的environ
    :return {'GET':get方法, 'POST':post方法, 'PUT':put方法, 'DELETE':delete方法}
    '''
    context = environ['fc.context']
    function = getattr(context, 'function')
    handler = getattr(function, 'handler')
    modName = handler.split('.')[0]

    mod = __import__(modName, globals(), locals())
    funcs = {}
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            if method == 'GET':
                funcs['GET'] = fn
            elif method == 'POST':
                funcs['POST'] = fn
            elif method == 'PUT':
                funcs['PUT'] = fn
            elif method == 'DELETE':
                funcs['DELETE'] = fn
    return funcs
        

