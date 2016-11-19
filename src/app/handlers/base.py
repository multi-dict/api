'''
Base class
'''
import json
from tornado.web import RequestHandler
from tornado import gen
import settings


class BaseHandler(RequestHandler):
    '''
    Base class handler
    '''
    
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def get_body(self):
        '''
        Return request data
        '''
        body = self.request.body.decode('utf-8')
        if len(body) == 0:
            self.write('request body missing')
            return False
        try:
            data = json.loads(body)
            if 'session_token' not in data:
                data['session_token'] = None
            return data
        except ValueError:
            self.write("Invalid json")
            return False

    def client_error(self, error, status=400, messages=()):
        '''
        Write client error and finish request
        '''
        self.set_status(status)
        body = {'error': error}
        if len(messages) > 0:
            body['messages'] = list(messages)
        self.write(body)
        self.finish()

    def server_error(self, error, status=500):
        '''
        Write server error and finish request
        '''
        self.set_status(status)
        self.write({'error': error})
        self.finish()


    def prepare_json(self, data):
        '''
        Make data to writeable
        '''
        for k, val in data.items() if isinstance(data, dict) else enumerate(data):
            if isinstance(val, dict) or isinstance(val, list):
                data[k] = self.prepare_json(val)
            else:
                try:
                    json.dumps(val)
                    # data[k] = val
                except (TypeError, OverflowError, ValueError):
                    data[k] = str(val)
        return data

    def write(self, response):
        '''
        @override
        '''
        data = self.prepare_json(response)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
        super(BaseHandler, self).write(data)

    def data_received(self, chunk):
        '''
        Abstract functions must override
        '''
        super(BaseHandler, self).data_received(chunk)
