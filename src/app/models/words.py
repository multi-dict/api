'''
Word
'''
from app.models.base import BaseModel
from tornado import gen
from . import POOL

class Word(BaseModel):
    '''
    Word Model
    '''
    @classmethod
    @gen.coroutine
    def get(cls, word_id=None):
        '''
        Return with a word
        '''
        cursor = yield POOL.execute('SELECT description, sex, source, word, language_id AS language FROM words_word WHERE id = %s', word_id)
        return cursor.fetchone()


    @classmethod
    @gen.coroutine
    def find(cls, entity_id=None):
        '''
        Find words
        '''
        cursor = yield POOL.execute('SELECT id, word, language_id AS language FROM words_word WHERE entity_id = %s', entity_id)
        return cursor.fetchall()

    @classmethod
    @gen.coroutine
    def create(cls, args):
        '''
        Insert a word into database
        '''
        args = tuple(args)
        cursor = yield POOL.execute('INSERT INTO words_word (entity_id, language_id, sex, description, source, word) VALUES (%s, %s, %s, %s, %s, %s);SELECT LAST_INSERT_ID() AS id;', args)
        word = yield cls.get(word_id=cursor.fetchone()['id'])
        return word

class Entity(BaseModel):
    '''
    Entity Model
    '''
    @classmethod
    @gen.coroutine
    def create(cls, dictionary_id=None):
        cursor = yield POOL.execute('INSERT INTO words_entity (dictionary_id) VALUES (%s);SELECT LAST_INSERT_ID() AS id;', dictionary_id)
        return cursor.fetchone()


    @classmethod
    @gen.coroutine
    def find(cls, dictionary_id=None):
        cursor = yield POOL.execute('SELECT id FROM words_entity WHERE dictionary_id = %s', dictionary_id)
        return cursor.fetchall()

