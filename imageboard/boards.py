from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from .db import pdb, Board, Post

bp = Blueprint('boards', __name__)
PAGE_SIZE = 10
POST_LIMIT = 150

def board_addpost(form, board, pdb):
    alias = Board.query.filter_by(alias=board).first().alias
    pdb.session.add(
        Post(body=form["body"], board_alias=alias)
    )
    pdb.session.commit()

def get_all_boards():
    return Board.query.all()

def get_posts_for_board(alias: str):
    posts = Post.query.filter_by(board_alias=alias).order_by(Post.created.asc()).all()
    if len(posts) > POST_LIMIT:
        for post in posts[POST_LIMIT:]:
            pdb.session.delete(post)
        pdb.session.commit()
    return posts

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("boards/index.html", boards=get_all_boards())

@bp.route('/<board>/', methods=['GET', 'POST'])
def board_paged(board):
    if request.method == 'POST':
        board_addpost(request.form, board, pdb)
    try:
        page = int((lambda x: x if x is not None else 0)(request.args.get('page', None)))
    except ValueError:
        abort(404)
    posts = get_posts_for_board(board)[page*PAGE_SIZE:page*PAGE_SIZE+PAGE_SIZE]
    if len(posts) == 0:
        abort(404)
    return render_template("boards/board_paged.html", posts=posts, boards=get_all_boards())

@bp.route('/<board>/catalog', methods=['GET', 'POST'])
def board_catalog(board):
    if request.method == 'POST':
        board_addpost(request.form, board, pdb)
    return jsonify([str(p) for p in get_posts_for_board(board)])
