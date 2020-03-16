from flask_sqlalchemy import SQLAlchemy


db  = SQLAlchemy()

def init_db(app):
    db = SQLAlchemy(app)

tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'), primary_key= True), #what it wants is the tablename
    db.Column('image_id', db.Integer, db.ForeignKey('Image.id'), primary_key=True)
    )

class Image(db.Model):
    __tablename__ = 'Image'
    
    id = db.Column(db.Integer, primary_key=True)
    image_title = db.Column(db.String(120))
    image_filename = db.Column(db.String(200), unique = True, nullable=False)

    comments = db.relationship('Comment', cascade='all,delete', backref='image', lazy=True)
    tags = db.relationship('Tag', cascade='all,delete',  secondary=tags, lazy='subquery', backref=db.backref('image', lazy=True))

    def __init__(self, title, filename):
        self.image_title = title
        self.image_filename = filename


class Tag(db.Model):
    __tablename__ = 'Tag'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(120), unique=True)

    def __init__(self, tag_name):
        self.tag_name = tag_name
class Comment(db.Model):
    __tablename__ = 'Comment'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('Image.id'), nullable=False)
    comment_text = db.Column(db.String(120))    

    def __init__(self, comment):
        self.comment_text = comment        
