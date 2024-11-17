#!/usr/bin/env python3
""" Define a class to manage the API authentication
            using Session based authentication
            with expiration date to a
            session ID
            + storing the session in a DB
"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session based authentication system,
        based on Session ID stored in database
    """

    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession
            and returns the Session ID

        Args:
            user_id (str, optional) . Defaults to None.
        """

        if not user_id:
            return None

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        new_session = UserSession(session_id=session_id, user_id=user_id)

        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession
                in the database based on session_id

        Args:
            session_id (_type_, optional): _description_. Defaults to None.
        """
        try:
            sessions_list = UserSession.search({"session_id": session_id})
        except Exception as e:
            return None

        if not sessions_list:
            return None

        return sessions_list[0]

    def destroy_session(self, request=None) -> bool:
        """delete a user session from the database
        """

        if request is None:
            return None

        session_id = self.session_cookie(request)
        if not session_id:
            return None

        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        user_session[0].remove()
        return user_session.user_id
