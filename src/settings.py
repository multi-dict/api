'''
Application settings
'''
import os
import config

ROUTES = (
    (r'/login', 'app.handlers.users.LoginHandler'),
    (r'/dictionaries', 'app.handlers.dictionaries.DictionaryHandler'),
    (r'/entities', 'app.handlers.words.EntityHandler'),
    (r'/words', 'app.handlers.words.WordHandler'),
    (r'/words/([^/]*)', 'app.handlers.words.WordHandler'),
)

DEBUG = os.environ.get('DEBUG', False)
PORT = os.environ.get('PORT', 5001)

DATABASE = {
    'NAME': config.DB_NAME,
    'USER': config.DB_USER,
    'PASSWORD': config.DB_PASSWORD,
    'HOST': config.DB_HOST,
    'PORT': int(config.DB_PORT),
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
