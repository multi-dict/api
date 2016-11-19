'''
Users
'''
from app.handlers.base import BaseHandler
from app.models.users import User
from app.utils.session import Session
from app.models.permission import Permission
from tornado import gen
from passlib.hash import django_pbkdf2_sha256 as handler

class LoginHandler(BaseHandler):
    '''
    Login RequestHandler
    '''

    @gen.coroutine
    def post(self):
        '''
        POST /login
        '''
        body = self.get_body()
        items = yield User.find(body['username'])
        if not items:
            self.client_error('Invalid username!', 403)
        else:
            user = items[0]
        if handler.verify(body['password'], user['password']):
            item = yield Session.create(user['id'])
            item['permissions'] = yield Permission.find(user_id=user['id'])
            item['is_superuser'] = user['is_superuser']
            self.write(item)
        else:
            self.client_error('Invalid password!', 403)
