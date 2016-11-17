import uuid
from app.models.users import User
from datetime import datetime, timezone
from tornado import gen

class Session():

    @classmethod
    @gen.coroutine
    def create(cls, user_id):
        session_token = str(uuid.uuid4()).replace('-', '')
        yield User.update({'id': user_id, 'session_token': session_token})
        return {'session_token' : session_token}
        
    @classmethod
    @gen.coroutine
    def check(cls, session_token):
        items = User.find(session_token=session_token)
        if not items:
            return False
        else:
            return items[0]

    @classmethod
    @gen.coroutine
    def destroy(cls, user_id):
        return User.update({'id': user_id, 'session_token': ''})
