'''
Aspplication entry point
'''
from tornado.web import Application
from tornado.ioloop import IOLoop
import settings

def main():
    '''
    Main method
    '''
    app = Application(settings.ROUTES, debug=settings.DEBUG)
    app.listen(settings.PORT)
    IOLoop.current().start()

if __name__ == "__main__":
    main()

