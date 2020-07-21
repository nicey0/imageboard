from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime as dt
from .db import pdb, Post

bp = Blueprint('boards', __name__)

@bp.route('/')
def index():
    return "Index"

@bp.route('/<board>/', methods=['GET', 'POST'])
def board_paged(board):
    if request.method == 'POST':
        title = request.form["title"]
        body = request.form["body"]
        post = Post(title, body, dt.utcnow())
        pdb.session.add(post)
        pdb.psession.commit()
    return f"Board: {board}"

@bp.route('/<board>/catalog')
def board_catalog(board):
    return f"Board catalog: {board}"
