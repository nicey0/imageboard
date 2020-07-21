from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime as dt
from .db import pdb, Post

bp = Blueprint('boards', __name__)
PAGE_SIZE = 10

def board_addpost(method, form, pdb):
    if method == 'POST':
        pdb.session.add(
            Post(body=form["body"])
        )
        pdb.session.commit()

@bp.route('/')
def index():
    return "Index"

@bp.route('/<board>/', methods=['GET', 'POST'])
def board_paged(board):
    board_addpost(request.method, request.form, pdb)
    try:
        page = int((lambda x: x if x is not None else 0)(request.args.get('page', None)))
    except ValueError:
        page = 0
    posts = Post.query.all()[page*PAGE_SIZE:page*PAGE_SIZE+PAGE_SIZE]
    return jsonify([str(p) for p in posts])

@bp.route('/<board>/catalog', methods=['GET', 'POST'])
def board_catalog(board):
    board_addpost(request.method, request.form, pdb)
    return jsonify([str(p) for p in Post.query.all()])
