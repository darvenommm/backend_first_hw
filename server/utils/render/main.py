from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from paths import Paths
from utils.env_variable import env


def add_new_template_directory(*paths: str) -> 'Path':
    total_path = Path(env.SERVER_PATH)

    for path in paths:
        total_path /= path

    return total_path


jinja_env = Environment(
    loader=FileSystemLoader((
        add_new_template_directory('views'),
        add_new_template_directory('entities', 'movies', 'views'),
    )),
    autoescape=select_autoescape(),
)


class Render:
    @staticmethod
    def render_template(name: str, **kwargs) -> str:
        return jinja_env.get_template(f'{name}.jinja').render(paths=Paths, **kwargs)
