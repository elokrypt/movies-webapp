# -*- coding: utf-8 -*-
"""
:filename sqlite_data_manager.py
:author Marcel 'elokrypt' Bz.
:email  elokrypt@keemail.me
:last_edited 5/26/2025, 11:23:14 PM
:summary [..]
"""

from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from ._data_manager_interface import DataManagerInterface
from ._data_models import Base, User, Movie
from ._data_models import create_new_user, verify_password
from ._data_models import create_movie_table
from ._data_models import MOVIE_X, insert_into_movie_table
from ._data_models import update_in_movie_table, delete_from_movie_table


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.engine = create_engine(db_file_name)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_users(self) -> list[User] | bool:
        """
        Returns all users in the database.
        """
        try:
            users: list[User]
            with self.Session() as session:
                users = session.scalars(select(User)).all()
            return users
        except SQLAlchemyError as err:
            print(err)
            return False

    def add_user(self, user_name, password) -> int:
        """
        Creates a new user, plus personal table, in the database.
        Returns :user_id on success, otherwise -1.
        """
        user: User
        try:
            # create a new user
            user = create_new_user(name=user_name, password=password)
            # add the new user to the database
            with self.Session.begin() as session:
                session.add(user)
            # query the new user from the database
            with self.Session() as session:
                user = session.execute(
                    select(User).where(User.name == user_name)
                ).first()[0]
            # dynamically create the database model
            # [ignoring return value here, ...]
            create_movie_table(user.id)
            # creating the associated table
            Base.metadata.create_all(self.engine)
            return user.id
        except SQLAlchemyError as err:
            print(err)
            return -1

    def verify_user(self, user_name, password) -> int:
        """
        Verifies a user, if password matches.
        Returns the :user_id as integer.
        """
        user: User
        try:
            user: User
            with self.Session() as session:
                user = session.execute(
                    select(User).where(User.name == user_name)
                ).first()[0]
            if user:
                if verify_password(password=password, hash=user.password):
                    return user.id
            return -1
        except SQLAlchemyError as err:
            print(err)
            return -1

    def get_user_movies(self, user_id: int) -> list[Movie] | bool:
        """
        Returns a user's movie information in the database.
        """
        try:
            movies: list[Movie]
            movie_tablename: str = MOVIE_X.format(user_id)
            stmt: str = text(f"SELECT * from {movie_tablename}")
            with self.Session() as session:
                movies = session.execute(stmt).all()
            return movies
        except SQLAlchemyError as err:
            print(err)
            return False

    def add_movie(self, user_id: int, movie: dict) -> bool:
        """
        Adds a movie to the user's movie table.
        """
        movie: Movie
        try:
            stmt: str = insert_into_movie_table(user_id, movie)
            with self.Session.begin() as session:
                session.execute(text(stmt))
            return True
        except SQLAlchemyError as err:
            print(err)
            return False

    def delete_movie(self, user_id: int, movie_id: int) -> bool:
        """
        Deletes a movie from the user's movies database.
        """
        try:
            stmt: str = delete_from_movie_table(user_id, movie_id)
            with self.Session.begin() as session:
                session.execute(text(stmt))
            return True
        except SQLAlchemyError as err:
            print(err)
            return False

    def update_movie(self, user_id: int, movie: dict) -> bool:
        """
        Updates a movie from the user's movies database.
        """
        try:
            stmt: str = update_in_movie_table(user_id, movie)
            with self.Session.begin() as session:
                session.execute(text(stmt))
            return True
        except SQLAlchemyError as err:
            print(err)
            return False
