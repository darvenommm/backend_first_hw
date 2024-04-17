"""Parser for html."""
from typing import Optional

import requests
from bs4 import BeautifulSoup


class HtmlParser:
    """Class for html parsing."""

    @staticmethod
    def parse_by_request(url: str, queries: Optional[dict[str, str]] = None) -> BeautifulSoup:
        """Parse html page by request url.

        Args:
            url: page url.
            queries: extra GET queries. Defaults to None.

        Returns:
            BeautifulSoup: Parsed html.
        """
        queries = queries if queries else {}
        page_text = requests.get(url, queries, timeout=10).text

        return BeautifulSoup(page_text, 'html.parser')
