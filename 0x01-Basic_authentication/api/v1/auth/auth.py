#!/usr/bin/env python3
"""
This module has the auth class.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    The  Auth class manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if auth is required.
        """
        if path is None:
            return True
        if len(excluded_paths) == 0 or excluded_paths is None:
            return True
        for value in excluded_paths:
            if value[-1] == '/':
                value = value[:len(value) - 1]
            if path[-1] == '/':
                path = path[:len(path) - 1]
            if path == value:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        This method gets authorization header.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method return a user from the request.
        """
        return None
