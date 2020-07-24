from .db import pdb, Board, Post, UIDOrigin, Response
from werkzeug.utils import secure_filename
from os import path
from hashlib import md5
from imageboard import app

PAGE_SIZE = 10
POST_LIMIT = 150
EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webm'}

def get_all_boards():
    return Board.query.all()

def get_page(args):
    return int((lambda x: x if x is not None else 0)(args.get('page', None)))

def get_posts_for_board(alias: str, page: int=-1):
    posts = Post.query.filter_by(board_alias=alias).order_by(Post.created.desc()).all()
    if page > -1:
        posts = posts[page*PAGE_SIZE:page*PAGE_SIZE+PAGE_SIZE]
    if len(posts) > POST_LIMIT:
        for post in posts[POST_LIMIT:]:
            pdb.session.delete(post)
        pdb.session.commit()
    return posts

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in EXTENSIONS

def get_uid():
    pdb.session.add(UIDOrigin())
    pdb.session.commit()
    uid = UIDOrigin.query.order_by(UIDOrigin.origin.desc()).first()
    return md5(bytes(uid.origin)).hexdigest()[:32]

def board_addpost(form, files, board):
    alias = Board.query.filter_by(alias=board).first().alias
    file = files.get('file-in', None)
    filename = filetype = None
    if file and file != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filetype = file.mimetype.split('/')[1]
        file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    pdb.session.add(
        Post(uid=get_uid(), body=form["body"], board_alias=alias, filename=filename, filetype=filetype)
    )
    pdb.session.commit()