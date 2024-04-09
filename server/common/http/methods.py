from typing import TypeAlias, Literal


HttpMethodsType: TypeAlias = (
    Literal['GET']
    | Literal['POST']
    | Literal['PUT']
    | Literal['PATCH']
    | Literal['DELETE']
    | Literal['HEAD']
    | Literal['OPTIONS']
    | Literal['TRACE']
    | Literal['CONNECT']
)

http_methods = (
    'GET', 'POST', 'PUT',
    'PATCH', 'DELETE', 'HEAD',
    'OPTIONS', 'TRACE', 'CONNECT',
)
