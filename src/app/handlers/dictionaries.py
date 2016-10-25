'''
Dictionary
'''
from app.handlers.base import BaseHandler
from app.models.dictionary import Dictionary
from tornado import gen


class DictionaryHandler(BaseHandler):
    '''
    Dictionary RequestHandler
    '''

    @gen.coroutine
    def get(self):
        '''
        GET /dictionary
        '''
        items = yield Dictionary.all()
        self.write({'dictionaries':items})
