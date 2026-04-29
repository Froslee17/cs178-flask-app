# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *
from dynamoCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/movies")
def movies():
    query = "SELECT * FROM movies LIMIT 20;"
    results = execute_query(query)
    return render_template("movies.html", movies=results)

@app.route("/movie-details")
def movie_details():
    query = """
        SELECT movies.title, genres.genre_name
        FROM movies
        JOIN genres ON movies.genre_id = genres.genre_id
        LIMIT 20;
    """
    results = execute_query(query)
    return render_template("movie_details.html", movies=results)

@app.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        query = "INSERT INTO movies (title, year) VALUES (%s, %s)"
        execute_query(query, (title, year))
        return redirect(url_for('movies'))
    return render_template('add_movie.html')

@app.route('/delete-movie/<int:id>')
def delete_movie(id):
    query = "DELETE FROM movies WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('movies'))

@app.route('/update-movie/<int:id>', methods=['GET', 'POST'])
def update_movie(id):
    if request.method == 'POST':
        title = request.form['title']
        query = "UPDATE movies SET title = %s WHERE id = %s"
        execute_query(query, (title, id))
        return redirect(url_for('movies'))
    return render_template('update_movie.html', id=id)

@app.route("/watchlist")
def watchlist():
    username = "alex"
    items = get_watchlist(username)
    return render_template("watchlist.html", items=items)


@app.route("/add-watchlist/<int:movie_id>/<title>")
def add_watchlist(movie_id, title):
    username = "alex"
    add_to_watchlist(username, movie_id, title)
    flash("Movie added to watchlist!", "success")
    return redirect(url_for("watchlist"))


@app.route("/mark-watched/<movie_id>")
def mark_watched(movie_id):
    username = "alex"
    update_watchlist_status(username, movie_id, "Watched")
    flash("Movie marked as watched!", "info")
    return redirect(url_for("watchlist"))


@app.route("/delete-watchlist/<movie_id>")
def delete_watchlist(movie_id):
    username = "alex"
    delete_from_watchlist(username, movie_id)
    flash("Movie removed from watchlist!", "warning")
    return redirect(url_for("watchlist"))

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
