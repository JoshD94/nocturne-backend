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

# Many to many relationship association table between Query and Genre
association_table5 = db.Table(
    "query_genre_association",
    db.Model.metadata,
    db.Column("query_id", db.Integer, db.ForeignKey("queries.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"))
)

# Many to many relationship association table between Song and Genre
association_table8 = db.Table(
    "song_genre_association",
    db.Model.metadata,
    db.Column("song_id", db.Integer, db.ForeignKey("songs.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"))
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
            'queries': [query.serialize() for query in self.queries],
        }

    def simple_serialize(self):
        '''
        Serialize the User object without songs, and genres
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
    mood = db.Column(db.String(80), default='')
    genres = db.relationship(
        "Genre", secondary=association_table8, back_populates="songs")

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
            'mood': self.mood,
            'genres': [genre.serialize() for genre in self.genres],
        }

    def simple_serialize(self):
        '''
        Serialize the Song object without moods, and genres
        '''
        return {
            'id': self.id,
            'title': self.title,
            'likes': self.likes,
            'user_id': self.user_id,
        }

    def get_mood_vector(self):
        '''
        Get the mood vector of the song
        '''
        if self.mood == '':
            return None
        return self.convert_str_vector(self.mood)

    def convert_str_vector(self, str):
        '''
        Convert a string to a 2D vector of integers
        '''
        red = ["enraged", "terrified", "panicked", "shocked", "impassioned", "hyper", "livid", "irate", "overwhelmed", "stressed", "annoyed", "pressured", "furious", "frightened", "anxious", "apprehensive", "irritated",
               "restless", "jealous", "scared", "angry", "jittery", "fomo", "confused", "envious", "repulsed", "frustrated", "embarrassed", "concerned", "tense", "contempt", "troubled", "worried", "nervous", "peeved", "uneasy"]
        blue = ["disgusted", "trapped", "insecure", "disheartened", "down", "bored", "humiliated", "ashamed", "lost", "disappointed", "meh", "tired", "pessimistic", "vulnerable", "disconnected", "forlorn", "sad", "fatigued",
                "guilty", "numb", "excluded", "spent", "discouraged", "disengaged", "depressed", "hopeless", "alienated", "nostalgic", "lonely", "apathetic", "miserable", "despair", "glum", "burned out", "exhausted", "helpless"]
        yellow = ["surprised", "awe", "exhilarated", "thrilled", "elated", "ecstatic", "excited", "determined", "successful", "amazed", "inspired", "empowered", "energized", "eager", "enthusiastic", "joyful", "productive",
                  "proud", "cheerful", "curious", "upbeat", "happy", "motivated", "optimistic", "pleasant", "focused", "alive", "confident", "engaged", "challenged", "pleased", "playful", "delighted", "wishful", "hopeful", "accomplished"]
        green = ["calm", "at ease", "understood", "respected", "fulfilled", "blissful", "good", "thoughtful", "appreciated", "supported", "loved", "connected", "relaxed", "chill", "compassionate", "included", "valued", "grateful",
                 "sympathetic", "comfortable", "empathetic", "content", "accepted", "moved", "mellow", "peaceful", "balanced", "safe", "secure", "blessed", "carefree", "tranquil", "thankful", "relieved", "satisfied", "serene"]
        if str in red:
            x = -red.index(str) % 6
            y = 6 - (red.index(str) // 6)
        elif str in blue:
            x = -blue.index(str) % 6
            y = -(6 - (blue.index(str) // 6))
        elif str in yellow:
            x = yellow.index(str) % 6
            y = 6 - (yellow.index(str) // 6)
        elif str in green:
            x = green.index(str) % 6
            y = -(6 - (green.index(str) // 6))
        else:
            return None
        return [x, y]


class Query(db.Model):
    '''
    Query model
    '''
    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(80), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.String(80), default='')
    genres = db.relationship(
        "Genre", secondary=association_table5, back_populates="queries")

    def __init__(self, **kwargs):
        '''
        Initialize a Query object
        '''
        self.text = kwargs.get('query')
        self.user_id = kwargs.get('user_id')

    def serialize(self):
        '''
        Serialize the Query object
        '''
        return {
            'id': self.id,
            'query': self.text,
            'user_id': self.user_id,
            'mood': self.mood,
            'genres': [genre.serialize() for genre in self.genres],
        }

########## Feature models ##########


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
