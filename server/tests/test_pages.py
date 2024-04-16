"""Module for testing pages."""
from uuid import uuid4

import requests
from bs4 import BeautifulSoup, Tag
from paths import Paths
from utils.env_variable import env


class TestPages:
    """Test pages."""

    imdb = 'tt2024469'

    def test_index_page(self):
        """Test index page."""
        form = self.get_parsed_html(Paths.home).find('form', class_='search_form')
        assert (form and isinstance(form, Tag))

        for tag in (form.label, form.input, form.button):
            assert tag

    def test_movies_page(self):
        """Test movies page."""
        html = self.get_parsed_html(Paths.movies, {'search_title': 'Stop'})
        list_ = html.find('ul', class_='movies__list')
        assert (list_ and isinstance(list_, Tag))

        li_items = list_.find_all('li')
        assert li_items

        for li_item in li_items:
            for tag in (li_item.h2, li_item.img):
                assert tag

    def test_movies_error_page(self):
        """Test movies page with incorrect search title."""
        html = self.get_parsed_html(Paths.movies, {'search_title': str(uuid4())})

        error_paragraph = html.find('p', class_='error')
        assert (error_paragraph and isinstance(error_paragraph, Tag))

    def test_my_movies_page(self):
        """Test my movies page creating and deleting some movie."""
        self.does_not_have_my_movies()
        self.add_movie()
        self.has_my_movies()
        self.remove_movie()
        self.does_not_have_my_movies()

    def does_not_have_my_movies(self) -> bool:
        """Check my movies page doesn't have any movies.

        Returns:
            bool: no movies - is a truth?.
        """
        html = self.get_parsed_html(Paths.my_movies)
        no_movies_paragraph = html.find('p', class_='movies__not-have')
        return (no_movies_paragraph is not None and isinstance(no_movies_paragraph, Tag))

    def has_my_movies(self) -> bool:
        """Check my movies page has some movies.

        Returns:
            bool: movies are - is a truth?.
        """
        html = self.get_parsed_html(Paths.my_movies)
        list_ = html.find('ul', class_='movies__list')
        return (list_ is not None and isinstance(list_, Tag))

    @staticmethod
    def get_parsed_html(path: str, queries: dict[str, str] | None = None) -> BeautifulSoup:
        """Parse html page by request to the server.

        Args:
            path: Endpoint path.
            queries: extra get queries. Defaults to None.

        Returns:
            BeautifulSoup: Parsed html.
        """
        queries = queries if queries else {}
        page_text = requests.get(f'{env.SERVER_DOMAIN}{path}', queries, timeout=10).text

        return BeautifulSoup(page_text, 'html.parser')

    def add_movie(self) -> None:
        """Add movie to mine."""
        path = f'{env.SERVER_DOMAIN}{Paths.my_movies}'
        requests.post(path, {'imdb': self.imdb}, timeout=10)

    def remove_movie(self) -> None:
        """Delete movie from mine."""
        path = f'{env.SERVER_DOMAIN}{Paths.my_movies}/{self.imdb}'
        requests.delete(path, timeout=10)
