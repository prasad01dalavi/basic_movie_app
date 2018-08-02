from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lmtech123@localhost:3306/movies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# let me know the changes in the database but i don't want to know, just
# setting some value (False) to avoid overhead warning

# create database object for the respective flask app
db = SQLAlchemy(app)


# class in python will be table in database
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # This is my primary key
    name = db.Column(db.String(20))  # This field stored the name of the movie
    # time of the movie
    timing = db.Column(db.String(200))
    # place where the movie will be played
    location = db.Column(db.String(200))

    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    # time_updated = Column(DateTime(timezone=True), onupdate=func.now())


@app.route('/')   # http://127.0.0.1:5000/
def index():
    all_data = Movies.query.all()  # Gives all data from Movies table
    return render_template('home.html', all_data=all_data)


@app.route('/add')   # http://127.0.0.1:5000/sign
def add():           # This url will be redirected
    return render_template('add_movie.html')


@app.route('/process', methods=['POST'])  # http://127.0.0.1:5000/process
def process():
    # accessing posted data
    print request.form
    name = request.form['name']
    timing = request.form['timing']
    location = request.form['location']

    # now save the data in database (pk will be auto incremented)
    movies_details = Movies(name=name, timing=timing, location=location)
    db.session.add(movies_details)  # adds the movies data into db session
    db.session.commit()             # and then save the data in database
    return redirect(url_for('index'))   # redirects to the view for /index


@app.route('/update')  # http://127.0.0.1:5000/process
def update():
    get_request_data = request.values
    movie_id = get_request_data['id'][0]
    # Now I have to return the movies record having id=movie_id

    requested_movie_object = Movies.query.get(movie_id)
    movie_name = requested_movie_object.name
    movie_timing = requested_movie_object.timing
    movie_location = requested_movie_object.location
    return 'somthing'

if __name__ == '__main__':
    app.run(debug=True)
