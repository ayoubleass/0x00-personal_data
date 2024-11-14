#!/usr/bin/env python3
"""
This module has the seesion auth class.
"""
import base64
import uuid
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    This class is the implementation of a session auth.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a new session.
        """
        if user_id is None and type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            Retrives a user id .
        """
        if session_id is None and type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
            Retrive the user using the session id.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
            Destroys the session.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
