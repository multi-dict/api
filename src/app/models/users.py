'''
User
'''
from app.models.base import BaseModel
from tornado import gen

from . import POOL

class User(BaseModel):
    '''
    User Model
    '''
    @classmethod
    @gen.coroutine
    def find(cls, username=None, session_token=None):
        if session_token is not None:
            cursor = yield POOL.execute('SELECT * FROM users_user WHERE session_token=%s', (session_token, ))
        else:
            cursor = yield POOL.execute('SELECT * FROM users_user WHERE username=%s', (username, ))
        item = cursor.fetchall()
        return item

    @classmethod
    @gen.coroutine
    def update(cls, args):
        query = 'UPDATE users_user SET '
        conditions = ()
        for key in args:
            if key != 'id':
                query += key + '=%s,'
                conditions = conditions + (args[key],)
        query = query[:-1]
        query += ' WHERE id=%s'
        conditions = conditions + (args['id'],)
        cursor = yield POOL.execute(query, conditions)
        items = cursor.fetchall()
        return items

