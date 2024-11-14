#!/usr/bin/env python3
"""Define a class to manage the API authentication using Basic Auth
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.base import Base
from models.user import User
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) \
            -> (str, str):  # type: ignore
        """retrieve the user email and password from the Base64 decoded value.
        """

        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) \
            -> TypeVar('User'):  # type: ignore
        """ get the user instance by its email and password
        """

        if (user_email is None) or (not isinstance(user_email, str)) or \
                (user_pwd is None) or (not isinstance(user_pwd, str)):
            return None

        try:
            users_list = User.search({"email": user_email})
        except Exception as e:
            return None

        if not users_list:
            return None

        usr = users_list[0]
        if usr.is_valid_password(user_pwd):
            return usr
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ overloads Auth and retrieves the User instance for a request:
        """
        if not request:
            return None

        auth_header = self.authorization_header(request)

        b64_auth_header = self.extract_base64_authorization_header(auth_header)

        decoded_b64_auth_header = self.decode_base64_authorization_header(
            b64_auth_header)

        usr_email, usr_password = self.extract_user_credentials(
            decoded_b64_auth_header)

        return self.user_object_from_credentials(usr_email, usr_password)
