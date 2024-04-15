"""Server entry point file."""
from http.server import HTTPServer
from os import getcwd
from pathlib import Path
from sys import path

path.append(Path(getcwd(), 'server').as_posix())

from utils.env_variable import env

from server import Server

server = HTTPServer((env.SERVER_HOST, env.SERVER_PORT), Server)


try:
    print('start')
    server.serve_forever()
except Exception as exception:
    print(str(exception))
finally:
    server.server_close()
