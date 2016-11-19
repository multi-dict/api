'''
Language
'''
from app.models.base import BaseModel
from tornado import gen
from . import POOL

class Language(BaseModel):
    '''
    Language Model
    '''
    @classmethod
    @gen.coroutine
    def get(cls, language_id=None):
        '''
        Return with a language
        '''
        cursor = yield POOL.execute('SELECT id, name, ISO_2  FROM languages_language WHERE id = %s', language_id)
        return cursor.fetchone()

    @classmethod
    @gen.coroutine
    def find(cls, dictionary_id=None):
        '''
        Return all Languages
        '''
        cursor = yield POOL.execute('\
            SELECT l.id AS id, name, ISO_2 \
            FROM languages_language l \
            INNER JOIN dictionaries_dictionary_languages dl\
            ON dl.language_id = l.id\
            WHERE dl.dictionary_id = %s', dictionary_id)
        return cursor.fetchall()
