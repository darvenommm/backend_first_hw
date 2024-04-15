"""Module with a helper class for work with paths."""
from os import getcwd
from pathlib import Path


class PathsHelper:
    """Helper class for work with paths."""

    __server_directory = f'{getcwd()}/server'

    @classmethod
    def create_absolute_path(cls, *paths: str) -> Path:
        """Create absolute path starting from server directory.

        Args:
            paths: segments of the path.

        Returns:
            Path: created path.
        """
        total_path = Path(cls.__server_directory)

        for path in paths:
            total_path /= path

        return total_path
