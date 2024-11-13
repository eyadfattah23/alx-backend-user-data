#!/usr/bin/env python3
"""Define a class to manage the API authentication using Basic Auth
"""
from api.v1.auth.auth import Auth

import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> str:
        """decodes the value of a Base64 string

        Args:
            base64_authorization_header (str):
                    basic64 part of the Authorization header to be decoded

        Returns:
            str: string representation of the Authorization header

            - None if base64_authorization_header is None.
            - None if base64_authorization_header is not a string.
            - None if base64_authorization_header is not a valid Base64
            - Otherwise, decoded value as UTF8 string
        """
        if not base64_authorization_header\
                or not isinstance(base64_authorization_header, str):
            return None

        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception as e:
            return None
