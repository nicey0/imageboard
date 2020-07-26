from flask import Blueprint, render_template, request, jsonify, abort, redirect, url_for
from .util import (get_all_boards, board_addpost, board_addreply, get_posts_for_board,
                   get_posts_with_replies_for_board, get_page)

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
    lposts = get_posts_with_replies_for_board(board, page=page)
    print(lposts)
    if page != 0 and len(lposts) == 0:
        abort(404)
    return render_template("boards/board_paged.html", posts=lposts, boards=get_all_boards(), cboard=board)

@bp.route('/<board>/reply/<uid>', methods=['GET' ,'POST'])
def reply(board, uid):
    if request.method == 'POST':
        board_addreply(uid, request.form, request.files, board)
    return redirect(url_for('boards.board_paged', board=board))

@bp.route('/<board>/catalog', methods=['GET', 'POST'])
def board_catalog(board):
    if request.method == 'POST':
        board_addpost(request.form, board)
    posts = get_posts_for_board(board)
    return render_template('boards/board_catalog.html', posts=posts, boards=get_all_boards(), cboard=board)
