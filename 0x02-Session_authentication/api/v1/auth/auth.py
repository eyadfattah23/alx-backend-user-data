#!/usr/bin/env python3
"""Define a class to manage the API authentication"""


from flask import request
from typing import List, TypeVar
from models.user import User
import re


class Auth:
    """manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Make sure that user only access authorized paths

        Args:
            path (str): path requested by user.
            excluded_paths (List[str]): paths prohibited to the user

        Returns:
            bool:
            True:
                    the path is not in the list of strings
                    path is None
                    excluded_paths is None or empty
                    excluded_paths is None or empty
            False:
                    otherwise

        Example for excluded_paths = ["/api/v1/stat*"]:

            /api/v1/users will return True
            /api/v1/status will return False
            /api/v1/stats will return False

        """

        if (path is None) \
                or (excluded_paths is None) \
                or (excluded_paths == []):
            return True

        if (path in excluded_paths) or (path+"/" in excluded_paths):
            return False

        for ex_path in excluded_paths:
            if '*' in ex_path:
                actual_path = ex_path.replace('*', '.*')
                if re.fullmatch(actual_path, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """check if the request has the required authorization header

        Args:
            request (flask.Request, optional): request by client.
                                                Defaults to None.

        Returns:
            str: the value of the authorization header key
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """returns None - request
        """
        return None
