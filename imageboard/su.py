from flask import Blueprint, g, session, request, redirect, url_for
from functools import wraps
from .db import pdb, Admin
from werkzeug.security import check_password_hash

bp = Blueprint('su', __name__, url_prefix='/su')

@bp.before_app_request
def load_su():
    g.su = session.get('su', None)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @wraps(view)
    def wrapper_view(**kwargs):
        if g.su is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapper_view
