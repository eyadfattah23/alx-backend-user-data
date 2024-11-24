#!/usr/bin/env python3
'''module for all authentication methods
'''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """encrypt a password using bcrypt
        into a salted hash

    Args:
        password (str)

    Returns:
        bytes: salted hash of the input password
    """

    # converting password to array of bytes
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    return bcrypt.hashpw(bytes, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """add a new user to the database

        Args:
            email (str): mandatory user email that will be
                            added to the database
            password (str): mandatory user email that will be
                            added to the database
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound as e:
            hashed_password = _hash_password(password)

            new_user = self._db.add_user(email, hashed_password)

            return new_user
