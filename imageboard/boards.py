from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime as dt
from .db import pdb, Post

bp = Blueprint('boards', __name__)
PAGE_SIZE = 10

@bp.route('/')
def index():
    return "Index"

@bp.route('/<board>/', methods=['GET', 'POST'])
def board_paged(board):
    try:
        page = int((lambda x: x if x is not None else 0)(request.args.get('page', None)))
    except ValueError:
        page = 0
    posts = Post.query.all()[page*PAGE_SIZE:page*PAGE_SIZE+PAGE_SIZE]
    return jsonify([str(p) for p in posts])

@bp.route('/<board>/catalog')
def board_catalog(board):
    if request.method == 'POST':
        body = request.form["body"]
        post = Post(body=body)
        pdb.session.add(post)
        pdb.session.commit()
    return jsonify([str(p) for p in Post.query.all()])
