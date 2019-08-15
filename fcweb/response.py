
class ResponseEntity:

    def __init__(self, statusCode, res = None):
        self.statusCode = statusCode
        self.res = res

    @staticmethod
    def status(statusCode):
        ''' 自定义状态
        '''
        return ResponseEntity(statusCode)

    @staticmethod
    def ok(self, res):
        ''' 200，成功
        '''
        return ResponseEntity('200', res)

    @staticmethod
    def badRequest(self, res):
        ''' 400，错误请求
        '''
        return ResponseEntity('400', res)

    @staticmethod
    def unauthorized(self, res):
        ''' 401，权限不足
        '''
        return ResponseEntity('401', res)

    @staticmethod
    def notFound(self, res):
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
        # 设置请求头
        if not self.response_headers:
            self.header()
        start_response(self.statusCode, self.response_headers)
        response = {}

        data = {}
        if isinstance(self.res, list):
            data = {'sum':len(self.res), 'list':self.res}
        if isinstance(self.res, str):
            data = {'msg': self.res}
        else :
            data = self.res

        if self.statusCode == '200':
            response['message'] = 'success'
            if token:
                response['token'] = token
        else:
            response['message'] = 'fail'
        
        response['data'] = data

        return response