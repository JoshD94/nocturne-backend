from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    '''
    User model
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)

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
            'email': self.email
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
            'user_id': self.user_id
        }
