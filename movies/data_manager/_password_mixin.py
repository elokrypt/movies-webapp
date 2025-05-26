# -*- coding: utf-8 -*-
"""
:filename password_hash.py
:author Marcel 'elokrypt' Bz.
:email  elokrypt@keemail.me
:last_edited 5/27/2025, 1:18:43 AM
:summary [..]
"""

import bcrypt


class Password(object):
    """Allows storing and retrieving password
    hashes using bcrypt."""

    def __init__(self, password: str, rounds=12, **kwds):
        self.salt = bcrypt.gensalt(rounds=rounds)
        self.hashed_password = bcrypt.hashpw(password.encode(), self.salt)
        self.value = self.hashed_password.decode()

    @staticmethod
    def checkpw(password: str, value: str) -> bool:
        if isinstance(password, str):
            password = password.encode()
        if isinstance(value, str):
            value = value.encode()

        return bcrypt.checkpw(password, value)
