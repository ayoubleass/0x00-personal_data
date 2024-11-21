#!/usr/bin/env python3
"""
This modulle has the hash_password function,which hash the password
and return a bytes value.
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from db import DB


def _hash_password(password: str) -> bytes:
    """
    Hashess the paassword.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a uuid.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        checks if the user is registred and
        Verifying the Password if is valid or not
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        is_valid = bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        if not is_valid:
            return False
        return True

    def create_session(self, email: str) -> str:
        """
        Generates  a session id and add it to the a user record.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        user.session_id = session_id
        return session_id
