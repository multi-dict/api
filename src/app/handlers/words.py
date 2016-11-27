'''
Word
'''
from app.handlers.base import BaseHandler
from app.models.words import Word, Entity
from tornado import gen
from app.models.users import User
from app.models.languages import Language

class EntityHandler(BaseHandler):
    '''
    Word RequestHandler
    '''

    @gen.coroutine
    def get(self):
        '''
        GET /entities
        '''
        user = yield User.find(session_token=self.get_argument('session_token', None))
        if not user:
            self.client_error('Invalid session token', 403)
            return
        dictionary_id = self.get_argument('dictionary_id', None)
        if not dictionary_id :
            self.client_error('Dictionary not found', 404)
            return
        items = yield Entity.find(dictionary_id=dictionary_id)
        for item in items:
            item['words'] = yield Word.find(entity_id=item['id'], query=self.get_argument('q', ''))
            for word in item['words']:
                word['language'] = yield Language.get(language_id=word['language'])
        self.write({'entities':items})

    @gen.coroutine
    def post(self):
        '''
        POST /entities
        Create an entity and add a word to it.
        '''
        body = self.get_body()
        user = yield User.find(session_token=body['session_token'])
        if not user:
            self.client_error('Invalid session token', 403)
            return
        del body['session_token']
        if 'dictionary_id' not in body or not body['dictionary_id']:
            self.client_error('Dictionary not found', 404)
            return
        if 'language_id' not in body or not body['language_id']:
            self.client_error('Language not found', 404)
            return
        if 'word' not in body or not body['word']:
            self.client_error('Word can not be empty', 400)
            return
        entity = yield Entity.create(dictionary_id=body['dictionary_id'])
        del body['dictionary_id']
        body['entity_id'] = entity['id']
        word = yield Word.create(args=body)
        self.write({'entitiy' : {'id' : entity['id'], 'word':word}})


class WordHandler(BaseHandler):
    '''
    Word RequestHandler
    '''
    @gen.coroutine
    def get(self, id):
        '''
        GET /words/{id}
        '''
        user = yield User.find(session_token=self.get_argument('session_token', None))
        if not user:
            self.client_error('Invalid session token', 403)
            return
        word = yield Word.get(word_id=id)
        if not word:
            self.client_error('Word not found', 404)
            return
        else:
            word['language'] = yield Language.get(language_id=word['language'])
            self.write({'word':word})

    @gen.coroutine
    def post(self):
        '''
        POST /words
        Add word to an existing entity.
        '''
        body = self.get_body()
        user = yield User.find(session_token=body['session_token'])
        if not user:
            self.client_error('Invalid session token', 403)
            return
        del body['session_token']
        if 'entity_id' not in body or not body['entity_id']:
            self.client_error('Entity not found', 404)
            return
        if 'language_id' not in body or not body['language_id']:
            self.client_error('Language not found', 404)
            return
        if 'word' not in body or not body['word']:
            self.client_error('Word can not be empty', 400)
            return
        word = yield Word.create(args=body)
        self.write({'word':word})

    @gen.coroutine
    def put(self, id):
        '''
        PUT /words/{id}
        '''
        body = self.get_body()
        user = yield User.find(session_token=body['session_token'])
        if not user:
            self.client_error('Invalid session token', 403)
            return
        del body['session_token']
        word = yield Word.get(word_id=id)
        if not word:
            self.client_error('Word not found', 404)
            return
        body['id'] = id
        word = yield Word.update(args=body)
        self.write({'word':word})

    @gen.coroutine
    def delete(self, id):
        '''
        DELETE /words/{id}
        '''
        user = yield User.find(session_token=self.get_argument('session_token', None))
        if not user:
            self.client_error('Invalid session token', 403)
            return
        word = yield Word.get(word_id=id)
        if not word:
            self.client_error('Word not found', 404)
            return
        success = yield Word.delete(word_id=id)
        self.write({'success':success})