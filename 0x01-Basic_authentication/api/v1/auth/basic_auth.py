#!/usr/bin/env python3
"""
This module has the BasicAuth class.
"""
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth
import re
import base64
import binascii
from models.user import User


class BasicAuth(Auth):
    """
    This class cover the basic auth process.
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        Parse the token from the header.
        """
        if isinstance(authorization_header, str):
            if not authorization_header.startswith("Basic"):
                return None
            match = re.match(r"^Basic\s+(.*)", authorization_header)
            if match:
                return match.group(1)
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode base64-encoded authorization header.
        """
        if isinstance(base64_authorization_header, str):
            try:
                cred = base64.b64decode(
                        base64_authorization_header, validate=True)
                return cred.decode('utf-8')
            except(binascii.Error, UnicodeDecodeError):
                return None

        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if isinstance(decoded_base64_authorization_header, str):
            match = re.match(r'(.*):(.*)', decoded_base64_authorization_header)
            if match:
                return match.group(1), match.group(2)
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Search for a user and returns the matched result.
        """
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None
        users = User.search({'email': user_email})
        if len(users) <= 1:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrives the user from the rquest obj.
        """
        auth_header = self.authorization_header(request)
        token = self.extract_base64_authorization_header(auth_header)
        cred = self.decode_base64_authorization_header(token)
        email, password = self.extract_user_credentials(cred)
        return self.user_object_from_credentials(email, password)
