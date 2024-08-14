#!/usr/bin/env python
""" password hash"""

import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a new user """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception as e:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user


def _hash_password(password: str) -> bytes:
    """ hash fxn """

    new_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return new_pass
