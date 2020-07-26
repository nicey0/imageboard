from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from .util import (get_all_boards, board_add_post_or_reply, get_posts_with_pages,
                   get_posts_with_replies_for_board)

bp = Blueprint('boards', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("boards/index.html", boards=get_all_boards())

@bp.route('/<board>')
def board_no_page(board):
    return redirect(url_for('boards.board_paged', board=board, page=0))
@bp.route('/<board>/<int:page>', methods=['GET', 'POST'])
def board_paged(board, page):
    if request.method == 'POST':
        board_add_post_or_reply(request.form, request.files, board)
    try:
        page = int(page)
    except ValueError:
        abort(404)
    lposts = get_posts_with_replies_for_board(board, page=page)
    if page != 0 and len(lposts) == 0:
        abort(404)
    return render_template("boards/board_paged.html", posts=lposts, boards=get_all_boards(), cboard=board,
                           page=page)

@bp.route('/<board>/reply/<uid>', methods=['GET' ,'POST'])
def reply(board, uid):
    if request.method == 'POST':
        board_add_post_or_reply(request.form, request.files, board, uid)
        try:
            page = int(request.form.get('page'))
        except ValueError:
            abort(404)
    return redirect(url_for('boards.board_paged', board=board, page=page))

@bp.route('/<board>/catalog', methods=['GET', 'POST'])
def board_catalog(board):
    pposts = get_posts_with_pages(board)
    print(*[post for post in pposts])
    return render_template('boards/board_catalog.html', pposts=pposts, boards=get_all_boards(), cboard=board)
