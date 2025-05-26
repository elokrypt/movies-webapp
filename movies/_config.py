# -*- coding: utf-8 -*-
"""
:filename _config.py
:author Marcel 'elokrypt' Bz.
:email  elokrypt@tuta.io
:last_edited 5/24/2025, 7:39:10 PM
:summary Book-Alchemy _config.py
"""

from datetime import timedelta
from logging.config import dictConfig
from pathlib import Path

#
#    ANSI colours are available by default in Windows version 1909 or newer.
#    These codes are the same as those used in a Unix/Linux/VT 100.
#
_ESC = {
    "rst": "\x1b[0m",
    #
    "bold": "\x1b[1m",
    "blink": "\x1b[5m",
    #
    "cyan": "\x1b[36m",
    "gray": "\x1b[90m",
    "yellow": "\x1b[33m",
    "green": "\x1b[32m",
}
_default_log_format: str = (
    f"{_ESC['gray']}[{_ESC['blink']}%(levelname)s"
    f"{_ESC['rst'] + _ESC['gray']}]\n\t"
    f"{_ESC['bold'] + _ESC['green']}Movies-App:\n\t\t"
    f"{_ESC['yellow']}%(message)s{_ESC['rst']}"
)


class DefaultConfig(object):
    """
    Book-Alchemy Flask application config defaults.
    """

    DEBUG: bool = True
    SECRET_KEY: str = (
        "7F9217E7D029D9F173D4B7FC4EDEBFEF5EF91716081262836E880B54FD5E0422"
    )
    SESSION_COOKIE_NAME: str = "session.cookie"
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    SESSION_PERMANENT: bool = False
    SESSION_TYPE: str = "filesystem"
    PERMANENT_SESSION_LIFETIME: timedelta(minutes=60)
    TEMPLATES_AUTO_RELOAD: bool = True
    PROVIDE_AUTOMATIC_OPTIONS: bool = False

    def __init__(self):
        dictConfig(
            {
                "version": 1,
                "formatters": {
                    "default": {
                        "format": _default_log_format,
                    },
                },
                "handlers": {
                    "wsgi": {
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                        "formatter": "default",
                    },
                },
                "root": {"level": "DEBUG", "handlers": ["wsgi"]},
            }
        )

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        data_dir = Path(__file__).parent.joinpath("db").as_posix()
        return f"sqlite:///{data_dir}/storage.sqlite"
