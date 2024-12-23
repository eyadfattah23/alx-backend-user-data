#!/usr/bin/env python3
"""Define a class to manage the API authentication
            using Session based authentication
"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
        - None: session_id is None
        - None: session_id is not a string
        - str: (the User ID) for the key session_id in user_id_by_session_id.
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value:

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """

        usr_id = self.user_id_for_session_id(self.session_cookie(request))

        return User.get(usr_id)

    def destroy_session(self, request=None) -> bool:
        """deletes the user session / logout
        """
        if not request:
            return False

        sessionID_by_cookie = self.session_cookie(request)
        if not sessionID_by_cookie:
            return False

        user_id = self.user_id_for_session_id(sessionID_by_cookie)

        if not user_id:
            return False

        del self.user_id_by_session_id[sessionID_by_cookie]

        return True
