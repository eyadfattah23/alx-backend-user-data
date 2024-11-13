#!/usr/bin/env python3
"""Define a class to manage the API authentication using Basic Auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Handles basic authentication

    Args:
        Auth (class): parent class for authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header

        Args:
            authorization_header (str): value of the Authorization header

        Returns:
            str: the Base64 part of the Authorization header.

            - None if authorization_header is None.
            - None if authorization_header is not a string.
            - None if authorization_header doesn't begin by "Basic "
            - Otherwise, return the value after Basic (after the space)
                    assume authorization_header contains only one Basic
        """

        if not authorization_header\
                or not isinstance(authorization_header, str) \
                or authorization_header.split(" ")[0] != "Basic":
            return None

        return authorization_header.split(" ")[1]
