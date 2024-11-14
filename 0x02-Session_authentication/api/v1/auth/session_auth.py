#!/usr/bin/env python3
"""Define a class to manage the API authentication
            using Session based authentication
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Handles Session based authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
        - None if user_id is None
        - None if user_id is not a string
        - str: Session ID using uuid module and uuid4()

        Note: 
        - The same user_id can have multiple Session ID
        """

        if not user_id or not isinstance(user_id, str):
            return None

        self.session_id = str(uuid.uuid4())
        self.user_id_by_session_id[self.session_id] = user_id
        return self.session_id