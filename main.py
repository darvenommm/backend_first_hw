from http.server import HTTPServer

from sys import path
from os import getcwd, environ
from pathlib import Path

from server import Server
from utils.env_variable import env

environ['SERVER_PATH'] = Path(getcwd(), 'server').as_posix()
path.append(environ['SERVER_PATH'])


server = HTTPServer((env.SERVER_HOST, env.SERVER_PORT), Server)


try:
    server.serve_forever()
except Exception as exception:
    print(str(exception))
finally:
    server.server_close()
