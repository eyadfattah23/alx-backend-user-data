#!/usr/bin/env python3
'''module for all authentication methods
'''

import bcrypt


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
