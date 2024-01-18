from src import app
from src import transforms

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


@app.route('/resize', methods=["POST"])
def resize():
    return transforms.resize(request.json)


@app.route('/delete_background', methods=["POST"])
def delete_background():
    return transforms.delete_background(request.json)


@app.route('/super_resolution', methods=["POST"])
def super_resolution():
    return transforms.super_resolution(request.json)


@app.route('/get_quality', methods=["POST"])
def get_quality():
    return transforms.get_quality(request.json)


@app.route('/pipeline', methods=["POST"])
def pipeline():
    return transforms.pipeline(request.json)
