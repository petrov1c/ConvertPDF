from app import app
from app import transforms

from flask import request
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Мой друг'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home', user=user, posts=posts)


@app.route('/ping')
def ping():
    return "It works!"


@app.route('/pdf_to_jpg', methods=["POST"])
def pdf_to_jpg():
    return transforms.pdf_to_jpg(request.data)


@app.route('/fix_pdf', methods=["POST"])
def fix_pdf():
    return transforms.fix_pdf(request.data)
