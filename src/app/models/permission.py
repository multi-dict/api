'''
Permission
'''
from app.models.base import BaseModel
from tornado import gen

from . import POOL

class Permission(BaseModel):
    '''
    Permission Model
    '''
    @classmethod
    @gen.coroutine
    def find(cls, user_id=None):
        cursor = yield POOL.execute('\
            SELECT name, codename \
            FROM auth_permission p\
            INNER JOIN users_user_user_permissions up \
            ON up.permission_id = p.id \
            WHERE up.user_id=%s', (user_id, ))
        item = cursor.fetchall()
        return item
