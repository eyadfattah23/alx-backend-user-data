#!/usr/bin/env python3
"""Define a class to manage the API authentication
            using Session based authentication
            with expiration date to a
            session ID
"""

from api.v1.auth.session_auth import SessionAuth
import uuid
from models.user import User
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class that inherits from SessionAuth
    to manage the expiration date on
    a session based authentication system
    """

    def __init__(self):
        """initialization method
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a Session ID by calling super()
        """
        sessionID = super().create_session(user_id)

        if not sessionID:
            return None
        self.user_id_by_session_id[sessionID] = {
            'user_id': user_id, 'created_at': datetime.now()}

        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """returns a User ID based on a Session ID

        Args:
            session_id (_type_, optional): _description_. Defaults to None.
        """
        if not session_id or not isinstance(session_id, str):
            return None

        session_dict = self.user_id_by_session_id.get(session_id, None)

        if not session_dict:
            return None

        user_id = session_dict.get('user_id')
        if self.session_duration <= 0:
            return user_id

        session_created_at = session_dict.get('created_at', None)
        if not session_created_at:
            return None

        if (session_created_at + timedelta(seconds=self.session_duration
                                           )) < datetime.now():
            return None

        return user_id
