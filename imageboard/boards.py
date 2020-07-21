from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime as dt
from .db import pdb, Post

bp = Blueprint('boards', __name__)

@bp.route('/')
def index():
    return "Index"

@bp.route('/<board>/', methods=['GET', 'POST'])
def board_paged(board):
    if request.method == 'POST':
        body = request.form["body"]
        post = Post(body=body)
        pdb.session.add(post)
        pdb.session.commit()
    return jsonify([str(p) for p in Post.query.all()])

@bp.route('/<board>/catalog')
def board_catalog(board):
    return f"Board catalog: {board}"
