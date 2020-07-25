from .db import pdb, Board, Post, UIDOrigin, Response
from werkzeug.utils import secure_filename
from os import path, remove, walk
from hashlib import md5
from imageboard import app

PAGE_SIZE = 10
POST_LIMIT = 150
EXTENSIONS = {'image': {'jpg', 'jpeg', 'png', 'gif'}, 'video': {'mp4', 'webm'}}

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
            delete_post(post)
        pdb.session.commit()
    return posts

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in set().union(*EXTENSIONS.values())

def get_uid():
    pdb.session.add(UIDOrigin())
    pdb.session.commit()
    uid = UIDOrigin.query.order_by(UIDOrigin.origin.desc()).first()
    return md5(bytes(uid.origin)).hexdigest()[:32]

def board_addpost(form, files, board):
    uid = get_uid()
    alias = Board.query.filter_by(alias=board).first().alias
    file = files.get('file-in', None)
    filename = filetype = ftt = None
    if file and file != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filetype = file.mimetype.split('/')[1]
        ftt = list(filter(lambda k: filetype in EXTENSIONS[k], EXTENSIONS))[0]
        file.save(path.join(app.config['UPLOAD_FOLDER'], uid+'.'+filetype))
    pdb.session.add(
        Post(uid=uid, body=form["body"], board_alias=alias, filename=filename, filetype=filetype, ftt=ftt)
    )
    pdb.session.commit()

def board_addreply(post_uid, form, files, board):
    uid = get_uid()
    file = files.get('rfile-in', None)
    filename = filetype = ftt = None
    if file and file != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filetype = file.mimetype.split('/')[1]
        ftt = list(filter(lambda k: filetype in EXTENSIONS[k], EXTENSIONS))[0]
        print(ftt)
        file.save(path.join(app.config['UPLOAD_FOLDER'], uid+'.'+filetype))
    pdb.session.add(
        Response(uid=uid, body=form["body"], filename=filename, filetype=filetype, ftt=ftt, post_uid=post_uid)
    )
    pdb.session.commit()

def delete_post(post):
    pdb.session.delete(post)
    if post.filename and post.filetype:
        print(post.body, post.uid, post.filetype)
        print("Removing", app.config['UPLOAD_FOLDER']+'/'+post.uid+'.'+post.filetype)
        remove(app.config['UPLOAD_FOLDER']+'/'+post.uid+'.'+post.filetype)

def clear_post_files():
    for (_, _, fs) in walk(app.config['UPLOAD_FOLDER']):
        [remove(app.config['UPLOAD_FOLDER']+'/'+file) for file in fs]
