import json
from db import db
from flask import Flask, request
from db import User, Genre, Mood, Query, Song
from openai import OpenAI

app = Flask(__name__)
db_filename = "nocturne.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# ---------- User Routes ---------- #


@app.route('/api/users/', methods=['GET'])
def get_users():
    """
    Endpoint for getting all users
    """
    users = [user.serialize() for user in User.query.all()]
    return success_response({"users": users})


@app.route('/api/users/', methods=['POST'])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    new_user = User(
        username=body.get('username'),
        email=body.get('email'),
        hashed_password=body.get('hashed_password')
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route('/api/users/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    """
    Endpoint for getting a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())


@app.route('/api/users/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    """
    Endpoint for deleting a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

# ---------- Song Routes ---------- #


@app.route('/api/songs/', methods=['GET'])
def get_songs():
    """
    Endpoint for getting all songs
    """
    songs = [song.serialize() for song in Song.query.all()]
    return success_response({"songs": songs})


@app.route('/api/songs/', methods=['POST'])
def create_song():
    """
    Endpoint for creating a song
    """
    body = json.loads(request.data)
    new_song = Song(
        title=body.get('title'),
        likes=body.get('likes', 0),
        user_id=body.get('user_id'),
        moods=[Mood.query.get(mood_id)
               for mood_id in body.get('mood_ids', [])],
        genres=[Genre.query.get(genre_id)
                for genre_id in body.get('genre_ids', [])],
    )
    db.session.add(new_song)
    db.session.commit()
    return success_response(new_song.serialize(), 201)


@app.route('/api/songs/<int:song_id>/', methods=['GET'])
def get_song(song_id):
    """
    Endpoint for getting a song
    """
    song = Song.query.filter_by(id=song_id).first()
    if song is None:
        return failure_response("Song not found")
    return success_response(song.serialize())


@app.route('/api/songs/<int:song_id>/', methods=['DELETE'])
def delete_song(song_id):
    """
    Endpoint for deleting a song
    """
    song = Song.query.filter_by(id=song_id).first()
    if song is None:
        return failure_response("Song not found")
    db.session.delete(song)
    db.session.commit()
    return success_response(song.serialize())

# ---------- Genre Routes ---------- #


@app.route('/api/genres/', methods=['GET'])
def get_genres():
    """
    Endpoint for getting all genres
    """
    genres = [genre.serialize() for genre in Genre.query.all()]
    return success_response({"genres": genres})


@app.route('/api/genres/', methods=['POST'])
def create_genre():
    """
    Endpoint for creating a genre
    """
    body = json.loads(request.data)
    new_genre = Genre(
        name=body.get('name')
    )
    db.session.add(new_genre)
    db.session.commit()
    return success_response(new_genre.serialize(), 201)


@app.route('/api/genres/<int:genre_id>/', methods=['GET'])
def get_genre(genre_id):
    """
    Endpoint for getting a genre
    """
    genre = Genre.query.filter_by(id=genre_id).first()
    if genre is None:
        return failure_response("Genre not found")
    return success_response(genre.serialize())


@app.route('/api/genres/<int:genre_id>/', methods=['DELETE'])
def delete_genre(genre_id):
    """
    Endpoint for deleting a genre
    """
    genre = Genre.query.filter_by(id=genre_id).first()
    if genre is None:
        return failure_response("Genre not found")
    db.session.delete(genre)
    db.session.commit()
    return success_response(genre.serialize())

# ---------- Mood Routes ---------- #


@app.route('/api/moods/', methods=['GET'])
def get_moods():
    """
    Endpoint for getting all moods
    """
    moods = [mood.serialize() for mood in Mood.query.all()]
    return success_response({"moods": moods})


@app.route('/api/moods/', methods=['POST'])
def create_mood():
    """
    Endpoint for creating a mood
    """
    body = json.loads(request.data)
    new_mood = Mood(
        mood=body.get('mood')
    )
    db.session.add(new_mood)
    db.session.commit()
    return success_response(new_mood.serialize(), 201)


@app.route('/api/moods/<int:mood_id>/', methods=['GET'])
def get_mood(mood_id):
    """
    Endpoint for getting a mood
    """
    mood = Mood.query.filter_by(id=mood_id).first()
    if mood is None:
        return failure_response("Mood not found")
    return success_response(mood.serialize())


@app.route('/api/moods/<int:mood_id>/', methods=['DELETE'])
def delete_mood(mood_id):
    """
    Endpoint for deleting a mood
    """
    mood = Mood.query.filter_by(id=mood_id).first()
    if mood is None:
        return failure_response("Mood not found")
    db.session.delete(mood)
    db.session.commit()
    return success_response(mood.serialize())

# ---------- Query Routes ---------- #


@app.route('/api/queries/', methods=['GET'])
def get_queries():
    """
    Endpoint for getting all queries
    """
    queries = [query.serialize() for query in Query.query.all()]
    return success_response({"queries": queries})


@app.route('/api/queries/', methods=['POST'])
def create_query():
    """
    Endpoint for creating a query
    """
    body = json.loads(request.data)
    new_query = Query(
        query=body.get('query'),
        user_id=body.get('user_id'),
        moods=[Mood.query.get(mood_id)
               for mood_id in body.get('mood_ids', [])],
        genres=[Genre.query.get(genre_id)
                for genre_id in body.get('genre_ids', [])],
    )
    db.session.add(new_query)
    db.session.commit()
    return success_response(new_query.serialize(), 201)


@app.route('/api/queries/<int:query_id>/', methods=['GET'])
def get_query(query_id):
    """
    Endpoint for getting a query
    """
    query = Query.query.filter_by(id=query_id).first()
    if query is None:
        return failure_response("Query not found")
    return success_response(query.serialize())


@app.route('/api/queries/<int:query_id>/', methods=['DELETE'])
def delete_query(query_id):
    """
    Endpoint for deleting a query
    """
    query = Query.query.filter_by(id=query_id).first()
    if query is None:
        return failure_response("Query not found")
    db.session.delete(query)
    db.session.commit()
    return success_response(query.serialize())


# to run flask app #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
