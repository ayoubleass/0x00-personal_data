#!/usr/bin/env python3
"""
This module has a  function that
returns a salted, hashed password.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Function that expects one string argument
    name password and returns a salted, hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password.
    """
    return checkpw(password.encode('utf-8'), hashed_password)
