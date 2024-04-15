"""Module with a helper class for work with paths."""
from pathlib import Path

from utils.env_variable import env


class PathsHelper:
    """Helper class for work with paths."""

    @staticmethod
    def create_directory_path(*paths: str) -> Path:
        """Create a path for some directory.

        Args:
            paths: paths for creating directory path.

        Returns:
            Path: created path.
        """
        total_path = Path(env.SERVER_PATH)

        for path in paths:
            total_path /= path

        return total_path
