'''
Dictionary
'''
from app.models.base import BaseModel
from tornado import gen
from . import POOL

class Dictionary(BaseModel):
    '''
    Dictionary Model
    '''

    @classmethod
    @gen.coroutine
    def all(cls):
        '''
        Return all Dictionarys
        '''
        cursor = yield POOL.execute('SELECT * FROM dictionaries_dictionaries')
        return cursor.fetchall()
