from http.server import HTTPServer
from os import environ

from request_handler import CustomHttpRequestHandler
from dotenv import load_dotenv
load_dotenv('.env')


HOST = environ.get('SERVER_HOST', '127.0.0.1')
PORT = int(environ.get('SERVER_PORT', '8000'))

server = HTTPServer((HOST, PORT), CustomHttpRequestHandler)


try:
    server.serve_forever()
except Exception as exception:
    print(str(exception))
finally:
    server.server_close()
