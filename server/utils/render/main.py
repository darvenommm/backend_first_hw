"""Module with a helper class for work with render html template."""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from paths import Paths
from utils.path import PathsHelper

jinja_env = Environment(
    loader=FileSystemLoader((
        PathsHelper.create_directory_path('views'),
        PathsHelper.create_directory_path('entities', 'movies', 'views'),
    )),
    autoescape=select_autoescape(),
)


class Render:
    """Helper class for work with render html template."""

    @staticmethod
    def render_template(path: str, **kwargs) -> str:
        """Render html template.

        Args:
            path: html template path.
            kwargs: add extra parameters to jinja render settings.

        Returns:
            str: html page in string.
        """
        return jinja_env.get_template(f'{path}.jinja').render(paths=Paths, **kwargs)
