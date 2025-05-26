# -*- coding: utf-8 -*-
"""
:filename __init__.py
:author Marcel 'elokrypt' Bz.
:email  elokrypt@keemail.me
:last_edited 5/24/2025, 8:14:43 PM
:summary [..]
"""

from os import getenv
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from requests import get

from movies._config import DefaultConfig
from movies.data_manager.sqlite_data_manager import SQLiteDataManager

load_dotenv()
# Setup Flask + configuration
app = Flask(__name__)
app.config.from_object(DefaultConfig())
# Setup server-side session handling
Session(app)
# Create a SQLiteDataManager instance
db = SQLiteDataManager(app.config["SQLALCHEMY_DATABASE_URI"])

API_URL: str = (
    f"https://www.omdbapi.com/?apikey={getenv('API_KEY')}&type=movie&t="
)


@app.route("/")
def index():
    user_id: int
    if not session.get("user_id"):
        return redirect("/login")

    user_id = int(session.get("user_id"))
    movies = db.get_user_movies(user_id=user_id)

    return render_template("index.jinja", logged_in=True, movies=movies)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name: str = request.form.get("user_name")
        password: str = request.form.get("password")
        user_id: int = db.verify_user(user_name=user_name, password=password)
        if user_id < 0:
            return render_template(
                "login.jinja",
                users=db.get_all_users(),
                error=("Invalid user-name or password !"),
            )
        else:
            session["user_id"] = user_id
            return redirect("/")
    return render_template("login.jinja", users=db.get_all_users(), error=False)


@app.route("/logout")
def logout():
    if session.get("user_id"):
        session.pop("user_id", None)
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name: str = request.form.get("user_name")
        password: str = request.form.get("password")
        user_id: int = db.add_user(user_name=user_name, password=password)
        if user_id < 0:
            return render_template(
                "register.jinja", error="An unknown error occured !"
            )
        else:
            session["user_id"] = user_id
            return redirect("/")
    return render_template(
        "register.jinja", users=db.get_all_users(), error=False
    )


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        if not session.get("user_id"):
            return redirect("/login")
        if not request.form.get("movie_title"):
            return "Invalid Request !", 500

        user_id: int = int(session.get("user_id"))
        movie_title: str = request.form.get("movie_title")
        movie_rating: float = float(request.form.get("rating"))

        movie_info = get(f"{API_URL}{movie_title}").json()
        if movie_info["Response"] == "False":
            return f"Could'nt find information about '{movie_title}'."
        else:
            if not movie_rating:
                if movie_info["imdbRating"] != "N/A":
                    movie_rating = float(movie_info["imdbRating"])
                else:
                    movie_rating = 0.00

            movie = {
                "title": movie_info["Title"],
                "year": movie_info["Year"],
                "rating": movie_rating,
                "poster": movie_info["Poster"],
                "plot": movie_info["Plot"],
                "director": movie_info["Director"],
            }

            if db.add_movie(user_id, movie):
                return redirect("/")
        return "An Error occured during the transaction !", 501
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("add_movie.jinja")


@app.route("/update_movie/<int:movie_id>", methods=["POST"])
def update_movie(movie_id: int):
    if not session.get("user_id"):
        return redirect("/login")
    if not request.form.get("rating"):
        return "Invalid request !", 500

    user_id: int = int(session.get("user_id"))
    update_data: dict = {
        "id": movie_id,
        "rating": float(request.form.get("rating")),
    }

    if db.update_movie(user_id, update_data):
        return redirect("/")
    return "An Error occured during the transaction !", 501


@app.route("/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id: int):
    if not session.get("user_id"):
        return redirect("/login")

    user_id: int = int(session.get("user_id"))

    if db.delete_movie(user_id, movie_id):
        return redirect("/")
    return "An Error occured during the transaction !", 501
