from flask import jsonify
import sqlite3


def get_movie(data):
    data = data[0]
    return {"title": data[0],
            "country": data[1],
            "release_year": data[2],
            "genre": data[3],
            "description": data[4]}


def get_movies_by_years(data):
    movies = []
    for movie in data:
        movies.append({"title": movie[0],
                       "release_year": movie[1]})
    return movies


def get_movies_by_genre(data):
    movies = []
    for movie in data:
        movies.append({"title": movie[0],
                       "genre": movie[1]})
    return movies


def get_movies_by_rating(data):
    movies = []
    for movie in data:
        movies.append({"title": movie[0],
                       "rating": movie[1],
                       "description": movie[2]})
    return movies


def get_by_pair(name1, name2):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT "cast"
        FROM netflix
        WHERE "cast" LIKE '%{name1}%'
        AND "cast" LIKE '%{name2}%'
        """
        cur.execute(query)
        data = cur.fetchall()
        result = []
        people = []
        for actors in data:
            people.extend(actors[0].split(", "))
        for actor in people:
            if people.count(actor) > 2 and \
                    actor not in result and \
                    actor not in (name1, name2):
                result.append(actor)
        return result


def get_movies_by_parameters(type_movie, release_year, listed_in):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = f"""
        SELECT title, description
        release_year, listed_in, "type"
        FROM netflix
        WHERE "type" = '{type}'
        AND release_year = '{release_year}'
        AND listed_in LIKE = '%{listed_in}%'
        LIMIT 100
        """
        cur.execute(query)
        data = cur.fetchall()
        movies = []
        for movie in data:
            movies.append({"title": movie[0],
                           "description": movie[1]})
        return jsonify(movies)
