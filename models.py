from flask_sqlalchemy import SQLAlchemy
from gallery import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db  = SQLAlchemy(app)

class Image(db.Model):
    image_title = db.Column()

class Tag(db.Model):
    tag_name = db.Column()

class Comment(db.Model):
    comment_text = db.Column()