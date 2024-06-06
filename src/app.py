from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import requests
from bs4 import BeautifulSoup
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import pandas as pd
import random
import re

app = Flask(__name__, static_url_path='/static')

# Set your own database name, username and password
db = "dbname='imdb2' user='postgres' host='localhost' password='your_password'"  # Update with your credentials
conn = psycopg2.connect(db)
cursor = conn.cursor()

bcrypt = Bcrypt(app)

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cur = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        cur.execute("SELECT * FROM users WHERE username = %s", (new_username,))
        unique = cur.fetchall()
        if len(unique) == 0:
            cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (new_username, new_password))
            conn.commit()
            flash('Account created!', 'success')
            return redirect(url_for("home"))
        else:
            flash('Username already exists!', 'error')
    return render_template("createaccount.html")

@app.route("/", methods=["POST", "GET"])
def home():
    cur = conn.cursor()
    # Getting 10 random rows from imdb_top_1000
    tenrand = "SELECT * FROM imdb_top_1000 ORDER BY random() LIMIT 8;"
    cur.execute(tenrand)
    movies = list(cur.fetchall())

    # Getting random Poster_ID from table imdb_top_1000
    randint = "SELECT Poster_ID FROM imdb_top_1000 ORDER BY random() LIMIT 1;"
    cur.execute(randint)
    randomNumber = cur.fetchone()[0]
    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == "POST":
            input_title = request.form["title"].lower() or ""
            input_genre = request.form["genre"].lower() or "any"
            input_rating = request.form["rating"] or "any"
            input_director = request.form["director"] or "any"

            if re.match(r"^[a-zA-Z0-9 ]+$", input_title):
                return redirect(url_for("query_movie", title=input_title, year="any", certificate="any", genre="any", rating="any", director="any"))
            else:
                return redirect(url_for("query_movie", title="any", year="any", certificate="any", genre=input_genre, rating=input_rating, director=input_director))  
        return render_template("index.html", content=movies, length=8, randomNumber=randomNumber)


@app.route("/movie/<title>/<year>/<certificate>/<genre>/<rating>/<director>", methods=["POST", "GET"])
def query_movie(title, year, certificate, genre, rating, director):
    cur = conn.cursor()
    conditions = []
    params = []

    if title != "any":
        conditions.append("Series_Title ILIKE %s")
        params.append(f"%{title}%")

    if year != "any":
        conditions.append("Released_Year = %s")
        params.append(year)

    if certificate != "any":
        conditions.append("Certificate = %s")
        params.append(certificate)

    if genre != "any":
        conditions.append("Genre ILIKE %s")
        params.append(f"%{genre}%")

    if rating != "any":
        conditions.append("IMDB_Rating >= %s")
        params.append(rating)

    if director != "any":
        conditions.append("Director ILIKE %s")
        params.append(f"%{director}%")

    if conditions:
        sqlcode = "SELECT * FROM imdb_top_1000 WHERE " + " AND ".join(conditions)
    else:
        sqlcode = "SELECT * FROM imdb_top_1000"

    cur.execute(sqlcode, params)
    movie_details = cur.fetchall()

    length = len(movie_details)

    return render_template("movie.html", content=movie_details, length=length)


@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password']

    insys = "SELECT * FROM users WHERE username = %s AND password = %s"
    cur.execute(insys, (username, password))

    ifcool = len(cur.fetchall()) != 0

    if ifcool:
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('Wrong password!', 'error')
    return redirect(url_for("home"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile")
def profile():
    cur = conn.cursor()
    if not session.get('logged_in'):
        return render_template('login.html')
    
    username = session['username']

    sql1 = "SELECT Series_Title, Released_Year, Certificate, Runtime, Genre, IMDB_Rating, Overview, Meta_score, Director, Star1, Star2, Star3, Star4, No_of_Votes, Gross, Local_Poster_Path, Poster_ID FROM favorites NATURAL JOIN imdb_top_1000 WHERE username = %s"
    cur.execute(sql1, (username,))
    favorites = cur.fetchall()

    return render_template("profile.html", content=favorites, length=len(favorites), username=username)


@app.route("/movie/<movieid>", methods=["POST", "GET"])
def movie_page(movieid):
    cur = conn.cursor()

    if not session.get('logged_in'):
        return render_template('login.html')
    
    if request.method == "POST":
        # Add to favorites
        username = session['username']
        try:
            sql1 = '''INSERT INTO favorites(username, Poster_ID) VALUES (%s, %s)'''
            cur.execute(sql1, (username, movieid))
            conn.commit()
            flash('Added to favorites!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error adding to favorites: {e}', 'error')

    sql1 = '''SELECT * FROM imdb_top_1000 WHERE Poster_ID = %s'''
    cur.execute(sql1, (movieid,))
    movie_details = cur.fetchone()

    if not movie_details:
        return abort(404, description="Resource not found")

    return render_template("mov.html", content=movie_details)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
