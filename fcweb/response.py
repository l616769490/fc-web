import json
from .right import encodeToken

class ResponseEntity:

    def __init__(self, statusCode, res = None):
        self.statusCode = statusCode
        self.res = res
        self.response_headers = [('Content-type', 'application/json')]

    @staticmethod
    def status(statusCode):
        ''' 自定义状态
        '''
        return ResponseEntity(statusCode)

    @staticmethod
    def ok(res):
        ''' 200，成功
        '''
        return ResponseEntity('200', res)

    @staticmethod
    def badRequest(res):
        ''' 400，错误请求
        '''
        return ResponseEntity('400', res)

    @staticmethod
    def unauthorized(res):
        ''' 401，权限不足
        '''
        return ResponseEntity('401', res)

    @staticmethod
    def notFound(res):
        ''' 404，未找到
        '''
        return ResponseEntity('404', res)
    
    def header(self, response_headers = [('Content-type', 'application/json')]):
        ''' 自定义HTTP头
        '''
        self.response_headers = response_headers
    
    def body(self, res):
        ''' 自定义HTTP内容
        '''
        self.res = res

    def build(self, start_response, token = None):
        ''' 生成请求
        :param start_response 函数计算的token
        :param token 返回给用户的token
        '''
        start_response(self.statusCode, self.response_headers)
        response = {}

        data = {}
        if isinstance(self.res, list):
            data = {'sum':len(self.res), 'list':self.res}
        elif isinstance(self.res, str):
            data = {'msg': self.res}
        else :
            data = self.res

        if self.statusCode == '200':
            response['message'] = 'success'
            if token:
                response['token'] = encodeToken(token)
        else:
            response['message'] = 'fail'
        
        response['data'] = data

        return response

    def __str__(self):
        return json.dumps({'status':self.statusCode, 'res':self.res}) 