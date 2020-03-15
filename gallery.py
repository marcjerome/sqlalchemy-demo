import os

from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
from models import db, init_db, Image

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
                db.session.add(db_image)
                db.session.commit()

                return redirect(url_for('index'))
            return 'no image found!'
            
        else:
            return "No image uploaded!"



@app.route('/')
def index():
    images = Image.query.all()
    return render_template('index.html', images=images)

    '''
        Image 
        Title 
        Image Tags
        Comments

        Image 
            image_title
        Tags
            tag_name
        Comments 
            comment_Text
        
        * An image can have many tags and a tag can have many images
        * An image can have many comments and a comment belongs to one image
        

    '''