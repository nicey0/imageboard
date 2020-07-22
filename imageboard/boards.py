from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .db import pdb, Board, Post

bp = Blueprint('boards', __name__)
PAGE_SIZE = 10

def board_addpost(form, pdb):
    pdb.session.add(
        Post(body=form["body"])
    )
    pdb.session.commit()

def get_all_boards():
    return Board.query.all()

def get_posts_for_board(alias: str):
    return Post.query.filter_by(board_alias=alias)

@bp.route('/')
def index():
    return jsonify([str(b) for b in get_all_boards()])

@bp.route('/<board>/', methods=['GET', 'POST'])
def board_paged(board):
    if request.method == 'POST':
        board_addpost(request.form, pdb)
    try:
        page = int((lambda x: x if x is not None else 0)(request.args.get('page', None)))
    except ValueError:
        page = 0
    return jsonify([str(p) for p in get_posts_for_board(board)
                    [page*PAGE_SIZE:page*PAGE_SIZE+PAGE_SIZE]])

@bp.route('/<board>/catalog', methods=['GET', 'POST'])
def board_catalog(board):
    if request.method == 'POST':
        board_addpost(request.form, pdb)
    return jsonify([str(p) for p in get_posts_for_board(board)])
