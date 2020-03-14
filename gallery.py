import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath(os.getcwd()) + '/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
  
app = Flask(__name__)
app.secret_key = 'somepreciouskey'
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/imageupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            
            if allowed_file(image.filename):
                image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
                return "Image is good"
            return 'no image found!'
            
            
        else:
            return "No image uploaded!"



@app.route('/')
def index():

    return render_template('index.html')

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