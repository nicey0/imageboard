from flask import Blueprint, render_template, request, jsonify, abort, url_for
from .util import (get_all_boards, board_addpost, get_posts_for_board, get_page, get_filetype_type)

bp = Blueprint('boards', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("boards/index.html", boards=get_all_boards())

@bp.route('/<board>/', methods=['GET', 'POST'])
def board_paged(board):
    if request.method == 'POST':
        board_addpost(request.form, request.files, board)
    try:
        page = get_page(request.args)
    except ValueError:
        abort(404)
    posts = get_posts_for_board(board, page=page)
    if page != 0 and len(posts) == 0:
        abort(404)
    posts = [(get_filetype_type(post), post) for post in posts]
    return render_template("boards/board_paged.html", posts=posts, boards=get_all_boards(), cboard=board)

@bp.route('/<board>/catalog', methods=['GET', 'POST'])
def board_catalog(board):
    if request.method == 'POST':
        board_addpost(request.form, board)
    posts = [(get_filetype_type(post), post) for post in get_posts_for_board(board)]
    return render_template('boards/board_catalog.html', posts=posts, boards=get_all_boards(), cboard=board)
