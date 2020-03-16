import os

from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
from models import db, init_db, Image, Comment, Tag

UPLOAD_FOLDER = os.path.abspath(os.getcwd()) + '/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
  
app = Flask(__name__)
app.secret_key = 'somepreciouskey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER

init_db(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imageupload/<filename>')
def send_image(filename):
    return send_from_directory('uploads', filename)

@app.route('/imageupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        if 'image' in request.files:
            image = request.files['image']
            
            if allowed_file(image.filename):
                image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
                title = request.form.get('title')
                filename = image.filename 
                
                db_image = Image(title, filename)
                if 'tag' in request.form:
                    tags = request.form.getlist('tag')
                    tag_list = Tag.query.filter(Tag.tag_name.in_(tags))

                    for tag in tag_list:
                        db_image.tags.append(tag)


                db.session.add(db_image)
                db.session.commit()

                return redirect(url_for('index'))
            return 'no image found!'
            
        else:
            return "No image uploaded!"


@app.route('/image/delete/<filename>', methods=['POST'])
def delete_image(filename):
    if request.method == 'POST':
        if 'delete' in request.form:
            image = Image.query.filter_by(image_filename=filename).first()
            os.remove(os.path.join(app.config['IMAGE_UPLOADS'], filename))
            db.session.delete(image)
            db.session.commit()
            return redirect(url_for('index'))
    return "Bad"

@app.route('/image/comment/<filename>', methods=['POST'])
def add_comment(filename):    
    if request.method == "POST":
        if 'add_comment' in request.form:
            image = Image.query.filter_by(image_filename=filename).first()
            comment_text = request.form.get('comment_text')
            image.comments.append(Comment(comment_text))
            db.session.add(image)
            db.session.commit()
            return redirect(url_for('index'))


@app.route('/image/edittitle/<filename>', methods=['POST', 'GET'])
def edit_title(filename):  
    print('Im here in edit title function!')
    if 'change_page' in request.form:
        print('Im here in change page!')
        return render_template('title.html', filename=filename)

    elif 'change_title' in request.form:
        print('Im here in change title!')
        image = Image.query.filter_by(image_filename=filename).first()
        image.image_title = request.form.get('title')
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/tag', methods=["POST"])
def add_tag():
    if request.method == "POST":
        if 'add_tag' in request.form:
            tag_name = request.form.get('tag_name')
            tag = Tag(tag_name)
            db.session.add(tag)
            db.session.commit() 
            
    return redirect(url_for('index'))


@app.route('/')
def index():
    images = Image.query.all()
    tags = Tag.query.all()
    return render_template('index.html', images=images, tags=tags)