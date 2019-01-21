from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from language_interfacing_handlers.cpp_preprocessing_handler import CppPreprocessingHandler

define('port', default=3000, help='port to listen on')

def main():
    """Construct and serve the tornado application."""
    app = Application(handlers= [
        ('/', CppPreprocessingHandler)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
