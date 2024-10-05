from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

########## Association tables for many to many relationships ##########

# Many to many relationship association table between User and Genre
association_table2 = db.Table(
    "user_genre_association",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"))
)

# Many to many relationship association table between User and Instrument
association_table3 = db.Table(
    "user_instrument_association",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("instrument_id", db.Integer, db.ForeignKey("instruments.id"))
)

# Many to many relationship association table between Query and Mood
association_table4 = db.Table(
    "query_mood_association",
    db.Model.metadata,
    db.Column("query_id", db.Integer, db.ForeignKey("queries.id")),
    db.Column("mood_id", db.Integer, db.ForeignKey("moods.id"))
)

# Many to many relationship association table between Query and Genre
association_table5 = db.Table(
    "query_genre_association",
    db.Model.metadata,
    db.Column("query_id", db.Integer, db.ForeignKey("queries.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"))
)

# Many to many relationship association table between Query and Instrument
association_table6 = db.Table(
    "query_instrument_association",
    db.Model.metadata,
    db.Column("query_id", db.Integer, db.ForeignKey("queries.id")),
    db.Column("instrument_id", db.Integer, db.ForeignKey("instruments.id"))
)

# Many to many relationship association table between Song and Mood
association_table7 = db.Table(
    "song_mood_association",
    db.Model.metadata,
    db.Column("song_id", db.Integer, db.ForeignKey("songs.id")),
    db.Column("mood_id", db.Integer, db.ForeignKey("moods.id"))
)

# Many to many relationship association table between Song and Genre
association_table8 = db.Table(
    "song_genre_association",
    db.Model.metadata,
    db.Column("song_id", db.Integer, db.ForeignKey("songs.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"))
)

# Many to many relationship association table between Song and Instrument
association_table9 = db.Table(
    "song_instrument_association",
    db.Model.metadata,
    db.Column("song_id", db.Integer, db.ForeignKey("songs.id")),
    db.Column("instrument_id", db.Integer, db.ForeignKey("instruments.id"))
)

########## Models ##########


class User(db.Model):
    '''
    User model
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    songs = db.relationship("Song", backref="user")
    queries = db.relationship("Query", backref="user")
    genres = db.relationship(
        "Genre", secondary=association_table2, back_populates="users")
    instruments = db.relationship(
        "Instrument", secondary=association_table3, back_populates="users")

    def __init__(self, **kwargs):
        '''
        Initialize a User object
        '''
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.hashed_password = kwargs.get('hashed_password')

    def serialize(self):
        '''
        Serialize the User object
        '''
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'songs': [song.serialize() for song in self.songs],
            'genres': [genre.serialize() for genre in self.genres],
            'instruments': [instrument.serialize() for instrument in self.instruments],
        }

    def simple_serialize(self):
        '''
        Serialize the User object without songs, genres, and instruments
        '''
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }


class Song(db.Model):
    '''
    Song model
    '''
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    moods = db.relationship(
        "Mood", secondary=association_table7, back_populates="songs")
    genres = db.relationship(
        "Genre", secondary=association_table8, back_populates="songs")
    instruments = db.relationship(
        "Instrument", secondary=association_table9, back_populates="songs")

    def __init__(self, **kwargs):
        '''
        Initialize a Song object
        '''
        self.title = kwargs.get('title')
        self.likes = kwargs.get('likes')
        self.user_id = kwargs.get('user_id')

    def serialize(self):
        '''
        Serialize the Song object
        '''
        return {
            'id': self.id,
            'title': self.title,
            'likes': self.likes,
            'user_id': self.user_id,
            'moods': [mood.serialize() for mood in self.moods],
            'genres': [genre.serialize() for genre in self.genres],
            'instruments': [instrument.serialize() for instrument in self.instruments],
        }

    def simple_serialize(self):
        '''
        Serialize the Song object without moods, genres, and instruments
        '''
        return {
            'id': self.id,
            'title': self.title,
            'likes': self.likes,
            'user_id': self.user_id,
        }


class Query(db.Model):
    '''
    Query model
    '''
    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query = db.Column(db.String(80), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    moods = db.relationship(
        "Mood", secondary=association_table4, back_populates="queries")
    genres = db.relationship(
        "Genre", secondary=association_table5, back_populates="queries")
    instruments = db.relationship(
        "Instrument", secondary=association_table6, back_populates="queries")

    def __init__(self, **kwargs):
        '''
        Initialize a Query object
        '''
        self.query = kwargs.get('query')
        self.user_id = kwargs.get('user_id')

    def serialize(self):
        '''
        Serialize the Query object
        '''
        return {
            'id': self.id,
            'query': self.query,
            'user_id': self.user_id,
            'moods': [mood.serialize() for mood in self.moods],
            'genres': [genre.serialize() for genre in self.genres],
            'instruments': [instrument.serialize() for instrument in self.instruments],
        }

########## Feature models ##########


class Mood(db.Model):
    '''
    Mood model
    '''
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mood = db.Column(db.String(80), default='')
    songs = db.relationship(
        "Song", secondary=association_table7, back_populates="moods")
    queries = db.relationship(
        "Query", secondary=association_table4, back_populates="moods")

    def __init__(self, **kwargs):
        '''
        Initialize a Mood object
        '''
        self.mood = kwargs.get('mood')

    def serialize(self):
        '''
        Serialize the Mood object
        '''
        return {
            'id': self.id,
            'mood': self.mood,
        }


class Genre(db.Model):
    '''
    Genre model
    '''
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(80), default='')
    users = db.relationship(
        "User", secondary=association_table2, back_populates="genres")
    songs = db.relationship(
        "Song", secondary=association_table8, back_populates="genres")
    queries = db.relationship(
        "Query", secondary=association_table5, back_populates="genres")

    def __init__(self, **kwargs):
        '''
        Initialize a Genre object
        '''
        self.genre = kwargs.get('genre')

    def serialize(self):
        '''
        Serialize the Genre object
        '''
        return {
            'id': self.id,
            'genre': self.genre,
        }


class Instrument(db.Model):
    '''
    Instrument model
    '''
    __tablename__ = 'instruments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instrument = db.Column(db.String(80), default='')
    users = db.relationship(
        "User", secondary=association_table3, back_populates="instruments")
    songs = db.relationship(
        "Song", secondary=association_table9, back_populates="instruments")
    queries = db.relationship(
        "Query", secondary=association_table6, back_populates="instruments")

    def __init__(self, **kwargs):
        '''
        Initialize a Instrument object
        '''
        self.instrument = kwargs.get('instrument')

    def serialize(self):
        '''
        Serialize the Instrument object
        '''
        return {
            'id': self.id,
            'instrument': self.instrument,
        }
