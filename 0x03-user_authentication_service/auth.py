#!/usr/bin/env python3
""" password hash"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


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
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ login validator """
        try:
            user = self._db.find_user_by(email=email)
            pass_check = bcrypt.checkpw(password, user.hashed_password)
        except Exception as e:
            return False
        return pass_check

    def create_session(self, email: str) -> str:
        """ creates a user login session """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id


def _hash_password(password: str) -> bytes:
    """ hash fxn """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    return str(uuid.uuid4())
