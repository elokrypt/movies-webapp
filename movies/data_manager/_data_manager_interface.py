# -*- coding: utf-8 -*-
"""
:filename _data_manager_interface.py
:author Marcel 'elokrypt' Bz.
:email  elokrypt@keemail.me
:last_edited 5/23/2025, 7:33:21 AM
:summary [..]
"""

from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """
        Returns all user-names in the database.
        """
        pass

    @abstractmethod
    def add_user(self, user_name: str, password: str):
        """
        Creates a new user, plus personal table, in the database.
        """
        pass

    @abstractmethod
    def verify_user(self, user_name, password) -> int:
        """
        Verifies a user, if password matches.
        Returns the :user_id as integer.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id: int):
        """
        Returns a user's movie information in the database.
        """
        pass

    @abstractmethod
    def add_movie(self, user_id: int, movie: dict):
        """
        Adds a movie to the user's movie table, in the database.
        """
        pass

    @abstractmethod
    def delete_movie(self, user_id: int, movie_id: int):
        """
        Deletes a movie from the user's movies database.
        """
        pass

    @abstractmethod
    def update_movie(self, user_id: int, movie: dict):
        """
        Updates a movie from the user's movies database.
        """
        pass
