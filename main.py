from http.server import HTTPServer
from request_handler import CustomHttpRequestHandler

import config


server = HTTPServer(config.SOCKET, CustomHttpRequestHandler)


try:
    server.serve_forever()
except Exception as exception:
    print(str(exception))
finally:
    server.server_close()
