from pathlib import Path
from os import getcwd

from jinja2 import Environment, FileSystemLoader, select_autoescape

from routes import paths

jinja_env = Environment(
    loader=FileSystemLoader(Path(getcwd()) / 'views'),
    autoescape=select_autoescape()
)

def render_template(html_file_name: str, **kwargs) -> str:
    return jinja_env.get_template(f'{html_file_name}.jinja').render(paths=paths, **kwargs)


__all__ = ('render_template',)
