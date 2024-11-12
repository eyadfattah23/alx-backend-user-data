#!/usr/bin/env python3
"""Define a class to manage the API authentication"""


from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: True if the path is not in the list of strings
        """

        """ if (path is None) \
                or (excluded_paths is None) \
                or (excluded_paths == []):
            return True

        if (path in excluded_paths) or (path+"/" in excluded_paths):
            return False
        else:
            return True """

        return (path is None or excluded_paths is None or excluded_paths == []
                or
                path not in excluded_paths
                and path + "/" not in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """_summary_

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request
        """
        return request
