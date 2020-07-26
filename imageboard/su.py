from flask import Blueprint, g, session, request, redirect, url_for, jsonify, flash
from functools import wraps
from .db import pdb, SuperTypes, Super, Post
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('su', __name__, url_prefix='/su')

@bp.before_app_request
def load_su():
    g.su = session.get('su', None)

def login_required(view):
    @wraps(view)
    def wrapper_view(**kwargs):
        if g.su is None:
            return redirect(url_for('index'))
        return view(**kwargs)
    return wrapper_view

def rank_required(rank: int):
    def rank_required_dec(view):
        def wrapper_view(**kwargs):
            if Super.query.filter_by(uid=g.su, rank=rank):
                return view(**kwargs)
            return redirect(url_for('index'))
        return wrapper_view
    return rank_required_dec

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        admin = Super(email=email, password=generate_password_hash(password), rank=SuperTypes.MOD)
        pdb.session.add(admin)
        pdb.session.commit()
    return jsonify([str(a) for a in Super.query.all()])

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
@login_required
def delete_post():
    # extra check
    uid = request.form["uid"]
    post = Post.query.filter_by(uid=uid).first()
    if len([Super.query.filter_by(uid=g.su).all()]) > 0 and post:
        pdb.session.delete(post)
        pdb.session.commit()
    return redirect(url_for('boards.board_paged', board=post.board_alias, page=0))

@bp.route('/add', methods=['GET', 'POST'])
@rank_required(SuperTypes.ADM)
def add_moderator():
    mod = Super(
        email=request.form["email"],
        password=generate_password_hash(request.form["password"]),
        rank=SuperTypes.MOD
    )
    pdb.session.add(mod)
    pdb.session.commit()
    return jsonify([str (a) for a in Super.query.all()])

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/tmp/logged')
def is_logged_in():
    return jsonify(str(Super.query.filter_by(uid=g.su).first()))
