from flask import Blueprint, g, session, request, redirect, url_for, jsonify, flash
from functools import wraps
from .db import pdb, SuperTypes, Super, Post, Board
from .util import find_post_page, add_super, confirm_application, deny_application
from werkzeug.security import check_password_hash

bp = Blueprint('su', __name__, url_prefix='/su')

@bp.before_app_request
def load_su():
    g.su = session.get('su', None)

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
                if su.rank == rank:
                    return view(**kwargs)
            print("UNAUTHORIZED")
            flash(f"Required rank: {str(rank).split('.')[-1]}")
            return redirect(url_for('index'), code=401)
        return rank_required_dec_wrapper
    return rank_required_dec

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        add_super(
            request.form["email"],
            request.form["password"],
            SuperTypes.APP
        )
    return jsonify([str(a) for a in Super.query.all()])

@bp.route('/add', methods=['GET', 'POST'])
@rank_required(SuperTypes.ADM)
def add_moderator():
    email = request.form["email"]
    confirm_application(email, SuperTypes.MOD)
    return jsonify([str (a) for a in Super.query.all()])

@bp.route('/remove', methods=['GET', 'POST'])
@rank_required(SuperTypes.ADM)
def deny_su_application():
    email = request.form["email"]
    deny_application(email)
    return jsonify([str (a) for a in Super.query.all()])

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        admin = Super.query.filter_by(email=email).first()
        if admin:
            if check_password_hash(admin.password, password):
                session['su'] = admin.uid
        else:
            flash("email/password combination failed.")
    return jsonify([str(a) for a in Super.query.all()])

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

@bp.route('/tmp/logged')
def is_logged_in():
    return jsonify(str(Super.query.filter_by(uid=g.su).first()))
