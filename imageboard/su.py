from flask import Blueprint, g, session, request, redirect, url_for, jsonify
from functools import wraps
from .db import pdb, Admin, Post
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

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        admin = Admin(email=email, password=generate_password_hash(password))
        pdb.session.add(admin)
        pdb.session.commit()
    return jsonify([str(a) for a in Admin.query.all()])

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        admin = Admin.query.filter_by(email=email).first()
        if check_password_hash(admin.password, password):
            session['su'] = admin.uid
    return jsonify([str(a) for a in Admin.query.all()])

@bp.route('/delete', methods=['POST'])
@login_required
def delete_post():
    # extra check
    uid = request.form["uid"]
    post = Post.query.filter_by(uid=uid).first()
    if len([Admin.query.filter_by(uid=g.su).all()]) > 0 and post:
        pdb.session.delete(post)
        pdb.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/tmp/logged')
def is_logged_in():
    return jsonify(g.su is not None)
