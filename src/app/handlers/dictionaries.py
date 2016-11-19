'''
Dictionary
'''
from app.handlers.base import BaseHandler
from app.models.dictionary import Dictionary
from tornado import gen
from app.models.users import User
from app.models.languages import Language

class DictionaryHandler(BaseHandler):
    '''
    Dictionary RequestHandler
    '''

    @gen.coroutine
    def get(self):
        '''
        GET /dictionary
        '''
        user = yield User.find(session_token=self.get_argument('session_token', None))
        if not user:
            self.client_error('Invalid session token', 403)
            return

        items = yield Dictionary.all()
        for item in items:
            item['languages'] = yield Language.find(dictionary_id=item['id']) 
        self.write({'dictionaries':items})
