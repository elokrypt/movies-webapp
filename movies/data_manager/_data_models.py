# -*- coding: utf-8 -*-
"""
:filename data_models.py
:author Marcel 'elokrypt' Bz.
:email  elokrypt@tuta.io
:last_edited 5/26/2025, 11:21:21 PM
:summary Movies data_models.py
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float

from ._password_mixin import Password

Base = declarative_base()


class User(Base):
    """
    A Database Model declaring a table to store
    user informations, with a PasswordHash extension.
    """

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


def create_new_user(name: str, password: str) -> User:
    hashed_password: str = Password(password=password).value
    return User(name=name, password=hashed_password)


def verify_password(password: str, hash: str):
    return Password.checkpw(password=password, value=hash)


class Movie(Base):
    """
    An abstract ORM Model declaring a table to
    store movie informations.
    """

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    poster = Column(String)
    plot = Column(Text)


def create_movie_table(user_id: int):
    """
    Dynamically creates an ORM Model-class,
    based on a given user_id.

    :param user_id -> :type int:
    Any integer associated with a :User:
    """
    tablename: str = f"movie_{user_id}"
    class_name: str = f"Movie{user_id}"
    Model = type(class_name, (Movie,), {"__tablename__": tablename})
    return Model


MOVIE_X: str = "movie_{}"


def delete_from_movie_table(user_id: int, movie_id: int) -> str:
    movie_tablename: str = MOVIE_X.format(user_id)
    raw_stmt: str = f"""
    DELETE FROM {movie_tablename}
    WHERE id = {movie_id}"""
    return raw_stmt


def insert_into_movie_table(user_id: int, movie: dict) -> str:
    movie_tablename: str = MOVIE_X.format(user_id)
    raw_stmt: str = f"""
    INSERT INTO {movie_tablename} ( title, director, year, rating, poster, plot )
    VALUES (
        '{movie["title"].replace("'", "''")}',
        '{movie["director"].replace("'", "''")}',
        {movie["year"]},
        {movie["rating"]},
        '{movie["poster"]}', 
        '{movie["plot"].replace("'", "''")}'
    )"""
    return raw_stmt


def update_in_movie_table(user_id: int, movie: dict) -> str:
    movie_tablename: str = MOVIE_X.format(user_id)
    raw_stmt: str = f"""
    UPDATE {movie_tablename} SET rating = {movie["rating"]}
    WHERE id = {movie["id"]}"""
    return raw_stmt
