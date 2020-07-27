from flask import Blueprint, g, session, request, redirect, url_for, flash, render_template, abort
from functools import wraps
from .db import pdb, SuperTypes, Super, Post, Board
from .util import find_post_page, add_super, confirm_application, deny_application, get_all_boards
from werkzeug.security import check_password_hash
from imageboard import limiter

bp = Blueprint('su', __name__, url_prefix='/su')

@bp.before_app_request
def load_su():
    g.su = session.get('su', None)
    if g.su:
        g.rank = Super.query.filter_by(uid=g.su).first().rank
    else:
        g.rank = None

def login_required(view):
    @wraps(view)
    def login_required_wrapper(**kwargs):
        if g.su is None:
            return redirect(url_for('index'))
        return view(**kwargs)
    return login_required_wrapper

def rank_required(rank: int):
    def rank_required_dec(view):
        @wraps(view)
        def rank_required_dec_wrapper(**kwargs):
            if g.su is not None:
                su = Super.query.filter_by(uid=g.su).first()
                if su and su.rank == rank:
                    return view(**kwargs)
            flash(f"Required rank: {str(rank).split('.')[-1]}")
            return redirect(url_for('index'), code=401)
        return rank_required_dec_wrapper
    return rank_required_dec

@bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        email = request.form["email"]
        if Super.query.filter_by(email=email).first() is not None:
            abort(403)
        add_super(
            email,
            request.form["password"],
            SuperTypes.APP
        )
        return redirect(url_for('index'), code=303)
    return render_template('su/signup.html', boards=get_all_boards())

@bp.route('/appdashboard')
def applicants_dashboard():
    return render_template('su/applicants_dashboard.html', boards=get_all_boards(), applicants=Super.query.filter_by(rank=SuperTypes.APP).all())

@bp.route('/add', methods=['POST'])
@rank_required(SuperTypes.ADM)
def add_moderator():
    email = request.form["email"]
    rank = {'adm': SuperTypes.ADM, 'mod': SuperTypes.MOD}[request.form["rank"]]
    confirm_application(email, rank)
    return redirect(url_for('su.applicants_dashboard'), code=303)

@bp.route('/remove', methods=['POST'])
@rank_required(SuperTypes.ADM)
def deny_su_application():
    email = request.form["email"]
    deny_application(email)
    return redirect(url_for('su.applicants_dashboard'), code=303)

@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("15 per minute")
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        admin = Super.query.filter_by(email=email).first()
        if admin:
            if check_password_hash(admin.password, password):
                session['su'] = admin.uid
                return redirect(url_for('index'), code=303)
        flash("email/password combination failed")
    return render_template('su/login.html', boards=get_all_boards())

@bp.route('/delete', methods=['POST'])
@rank_required(SuperTypes.MOD)
def delete_post():
    uid = request.form["uid"]
    post = Post.query.filter_by(uid=uid).first()
    board = Board.query.order_by(Board.alias.asc()).first().alias
    page = 0
    if len([Super.query.filter_by(uid=g.su).all()]) > 0 and post:
        pdb.session.delete(post)
        pdb.session.commit()
        page = find_post_page(post.board)
    return redirect(url_for('boards.board_paged', board=board, page=page), code=303)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/list')
def su_list():
    admins = Super.query.filter_by(rank=SuperTypes.ADM)
    mods = Super.query.filter_by(rank=SuperTypes.MOD)
    return render_template('su/su_list.html', boards=get_all_boards(), admins=admins, mods=mods)
