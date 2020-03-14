from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

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