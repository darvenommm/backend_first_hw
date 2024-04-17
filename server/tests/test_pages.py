"""Module for testing pages."""
import requests
from bs4 import Tag
from paths import Paths
from utils.env_variable import env
from utils.html_parser import HtmlParser

IMDB_FOR_TESTING = 'tt2024469'


def get_page_url(path: str) -> str:
    """Get page url for testing.

    Args:
        path: page url without domain.

    Returns:
        str: result url.
    """
    return f'{env.SERVER_DOMAIN}{path}'


class TestIndexPage:
    """Class for testing the index page."""

    def test(self) -> None:
        """Test index page."""
        url = get_page_url(Paths.home)
        form = HtmlParser.parse_by_request(url).find('form', class_='search_form')
        assert (form and isinstance(form, Tag))

        for tag in (form.label, form.input, form.button):
            assert tag


class TestMoviesPage:
    """Class for testing the movies page."""

    def test(self) -> None:
        """Test movies page."""
        html = HtmlParser.parse_by_request(get_page_url(Paths.movies), {'search_title': 'Stop'})
        list_ = html.find('ul', class_='movies__list')
        assert (list_ and isinstance(list_, Tag))

        li_items = list_.find_all('li')
        assert li_items

        for li_item in li_items:
            for tag in (li_item.h2, li_item.img):
                assert tag


class TestMoviePage:
    """Class for testing movie page."""

    def test(self) -> None:
        """Test movie page."""
        url = get_page_url(f'{Paths.movies}/{IMDB_FOR_TESTING}')
        movie_container = HtmlParser.parse_by_request(url).find('div', class_='movie')

        assert (movie_container and isinstance(movie_container, Tag))
        assert movie_container.find('h1')
        assert movie_container.find_all('p')


class TestMyMoviesPage:
    """Class for testing my movies page."""

    page_url = get_page_url(Paths.my_movies)

    @classmethod
    def test(cls) -> None:
        """Test my movie page."""
        assert cls.is_empty()
        cls.add_movie()
        assert not cls.is_empty()
        cls.remove_movie()
        assert cls.is_empty()

    @classmethod
    def add_movie(cls) -> None:
        """Add the test movie."""
        request_data = {'imdb': IMDB_FOR_TESTING}
        requests.post(cls.page_url, request_data, timeout=10)

    @classmethod
    def remove_movie(cls) -> None:
        """Remove the test movie."""
        requests.delete(f'{cls.page_url}/{IMDB_FOR_TESTING}', timeout=10)

    @classmethod
    def is_empty(cls) -> bool:
        """Check being empty page.

        Returns:
            bool: is empty or no.
        """
        p_element = HtmlParser.parse_by_request(cls.page_url).find('p', class_='movies__not-have')
        return (p_element is not None and isinstance(p_element, Tag))
