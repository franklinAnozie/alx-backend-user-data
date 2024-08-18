#!/usr/bin/env python3
""" Module of auths
"""

from flask import request
from typing import List, TypeVar
from models.user import User


class Auth():
    """ Authentication Class """

    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """ require auth method """
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user """
        return None

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ auth not required """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path = f"{path}/"
            if path not in excluded_paths:
                return True
        return False
