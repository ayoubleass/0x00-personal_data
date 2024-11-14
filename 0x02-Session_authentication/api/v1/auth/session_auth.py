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
