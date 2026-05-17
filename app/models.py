from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    statuses = db.relationship('UserAnimeStatus', backref='user', lazy=True)

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mal_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.String(50), nullable=True)
    
    statuses = db.relationship('UserAnimeStatus', backref='anime', lazy=True)

class UserAnimeStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False) # 'watching', 'completed', 'plan'
