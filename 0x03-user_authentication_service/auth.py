#!/usr/bin/env python3
'''module for all authentication methods
'''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


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


def _generate_uuid() -> str:
    """generate a new UUID
    Returns:
        str: a new uuid.uuid4 string
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ check the password with bcrypt.checkpw

        Args:
            email (str): mandatory user email that will be
                            added to the database
            password (str): password to check

        Returns:
            bool: If it matches return True. In any other case, return False.
        """

        try:
            usr = self._db.find_user_by(email=email)
        except Exception as e:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), usr.hashed_password)

    def create_session(self, email: str) -> str:
        """
            find the user corresponding to the email,
                generate a new UUID
                and store it in the database as the user’s session_id

        Args:
            email (str): user email to check if the user is already
                        existing

        Returns:
            str: a new session id
        """

        try:
            usr = self._db.find_user_by(email=email)
        except Exception as e:
            return None

        usr.session_id = _generate_uuid()

        return usr.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """retrieve user having the session id passed as argument

        Args:
            session_id (str): session id used to retrieve the user

        Returns:
            User: corresponding user to the session ID.
            None: if the session ID is None or no user is found,
        """
        if not session_id:
            return None

        try:
            usr = self._db.find_user_by(session_id=session_id)
        except Exception as exc:
            return None

        return usr
