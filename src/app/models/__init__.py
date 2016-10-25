'''
Models configuration
'''
from tornado_mysql import pools
from tornado_mysql.cursors import DictCursor
import settings

pools.DEBUG = settings.DEBUG

POOL = pools.Pool(
    dict(
        host=settings.DATABASE['HOST'],
        port=int(settings.DATABASE['PORT']),
        user=settings.DATABASE['USER'],
        passwd=settings.DATABASE['PASSWORD'],
        db=settings.DATABASE['NAME'],
        cursorclass=DictCursor,
        charset='utf8'
    ),
    max_idle_connections=1,
    max_recycle_sec=3
)
