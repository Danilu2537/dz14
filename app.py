from flask import Flask, jsonify
import sqlite3
from utils import *

app = Flask(__name__)


@app.route('/movie/<title>')
def api_title(title):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT title, country, 
        release_year, listed_in, description
        FROM netflix
        WHERE title LIKE "%{title}%"
        ORDER BY release_year DESC
        LIMIT 1
        """
        cur.execute(query)
        return jsonify(get_movie(cur.fetchall()))


@app.route('/rating/children')
def rating_children():
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating = 'G'
        LIMIT 100
        """
        cur.execute(query)
        return jsonify(get_movies_by_rating(cur.fetchall()))


@app.route('/movie/<int:year1>/to/<int:year2>')
def year_to_year(year1, year2):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT title, release_year
        FROM netflix
        WHERE title BETWEEN {year1} AND {year2}
        LIMIT 100
        """
        cur.execute(query)
        return jsonify(get_movies_by_years(cur.fetchall()))


@app.route('/genre/<genre>')
def get_by_genre(genre):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT title, description, listed_in, release_year
        FROM netflix
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY release_year DESC
        LIMIT 10
        """
        cur.execute(query)
        return jsonify(get_movies_by_genre(cur.fetchall()))


@app.route('/rating/adult')
def rating_adult():
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN ('R', 'NC-17')
        LIMIT 100
        """
        cur.execute(query)
        return jsonify(get_movies_by_rating(cur.fetchall()))


@app.route('/rating/family')
def rating_family():
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN ('G', 'PG', 'PG-13')
        LIMIT 100
        """
        cur.execute(query)
        return jsonify(get_movies_by_rating(cur.fetchall()))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
