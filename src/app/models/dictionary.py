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
        Return all Dictionaries
        '''
        cursor = yield POOL.execute('SELECT * FROM dictionaries_dictionary')
        return cursor.fetchall()
