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
        cursor = yield POOL.execute('SELECT id, description, gender, source, word, language_id AS language FROM words_word WHERE id = %s', word_id)
        return cursor.fetchone()


    @classmethod
    @gen.coroutine
    def find(cls, entity_id=None, query=''):
        '''
        Find words
        '''
        cursor = yield POOL.execute('SELECT id, word, description, gender, source, language_id AS language FROM words_word WHERE entity_id = %s AND word LIKE %s', (entity_id, '%'+query+'%',))
        data = cursor.fetchall()
        if len(data) > 0:
            cursor = yield POOL.execute('SELECT id, word, description, gender, source, language_id AS language FROM words_word WHERE entity_id = %s', (entity_id,))
        return cursor.fetchall()

    @classmethod
    @gen.coroutine
    def create(cls, args):
        '''
        Insert a word into database
        '''
        query = 'INSERT INTO words_word ('
        parms = ()
        values = ''
        for i, key in enumerate(args):
            query += key + ','
            values += '%s,'
            parms += (args[key], )
        query = query[:-1] 
        query += ') VALUES (' 
        query += values[:-1]
        query += ');SELECT LAST_INSERT_ID() AS id;'
        try:
            cursor = yield POOL.execute(query, parms)
            word = yield cls.get(word_id=cursor.fetchone()['id'])
            return word
        except Exception as e:
            return str(e)

    @classmethod
    @gen.coroutine
    def update(cls, args):
        query = 'UPDATE words_word SET '
        conditions = ()
        for key in args:
            if key != 'id':
                query += key + '=%s,'
                conditions = conditions + (args[key],)
        query = query[:-1]
        query += ' WHERE id=%s;SELECT LAST_INSERT_ID() AS id;'
        conditions = conditions + (args['id'],)
        try:
            cursor = yield POOL.execute(query, conditions)
            word = yield cls.get(word_id=args['id'])
            return word
        except Exception as e:
            return str(e)

    @classmethod
    @gen.coroutine
    def delete(cls, word_id=None):
        '''
        Find words
        '''
        try:
            cursor = yield POOL.execute('DELETE FROM words_word WHERE id = %s', word_id)
            cursor.fetchone()
            return True
        except Exception as e:
            return str(e)

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

