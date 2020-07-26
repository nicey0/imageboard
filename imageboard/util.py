from .db import pdb, SuperTypes, Super, Board, Post, UIDOrigin, Response
from flask import flash
from werkzeug.utils import secure_filename
from os import path, remove, walk
from hashlib import md5
from imageboard import app
from werkzeug.security import generate_password_hash

PAGE_SIZE = 10
POST_LIMIT = 150
EXTENSIONS = {'image': {'jpg', 'jpeg', 'png', 'gif'}, 'video': {'mp4', 'webm'}}

def get_all_boards():
    return Board.query.all()

def get_posts_for_board(alias: str, page: int=-1):
    posts = Post.query.filter_by(board_alias=alias).order_by(Post.created.desc()).all()
    if page > -1:
        posts = posts[page*PAGE_SIZE:page*PAGE_SIZE+PAGE_SIZE]
    if len(posts) > POST_LIMIT:
        for post in posts[POST_LIMIT:]:
            delete_post(post)
        pdb.session.commit()
    return posts

def get_posts_with_replies_for_board(alias: str, page: int=-1):
    posts = get_posts_for_board(alias, page=page)
    lposts = []
    for post in posts:
        lposts.append((post, list(post.responses)))
    return lposts

def get_posts_with_pages(board):
    pposts = []
    page = 0
    while True:
        posts = get_posts_for_board(board, page)
        if len(posts) == 0:
            break
        elif len(pposts) == page+1:
            pposts[page][1].append(posts)
        else:
            pposts.append([page, posts])
            page += 1
    return pposts

def find_post_page(post):
    board = post.board_alias
    page = 0
    while True:
        posts = get_posts_for_board(board)
        if len(posts) == 0:
            return -1
        if post in posts:
            return page
        page += 1

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in set().union(*EXTENSIONS.values())

def get_uid():
    pdb.session.add(UIDOrigin())
    pdb.session.commit()
    uid = UIDOrigin.query.order_by(UIDOrigin.origin.desc()).first()
    return md5(bytes(uid.origin)).hexdigest()[:32]

def board_add_post_or_reply(form, files, board, post_uid=''):
    error = False
    uid = get_uid()
    # Get body content, body is '' if empty
    body = form.get('body')
    # Get file, file.filename is '' if empty
    file = files.get('file-in')
    # Filter off the ones that aren't empty
    c = {'body': body, 'file': file.filename}
    to_flash = [k for k in list(filter(lambda k: c[k] == '', c))]
    if to_flash != []:
        [flash(f"Please fill '{k}' field") for k in to_flash]
        error = True
    # Get file information
    filename, filetype = secure_filename(file.filename), file.mimetype.split('/')[1]
    ftt = list(filter(lambda k: filetype in EXTENSIONS[k], EXTENSIONS))
    if ftt == []:
        flash("Illegal file type")
        error = True
    if error:
        return
    ftt = ftt[0]
    # Add post/reply
    if post_uid == '':
        _board_addpost(uid, body, filename, filetype, ftt, board)
    else:
        _board_addreply(uid, body, filename, filetype, ftt, post_uid)
    pdb.session.commit()
    file.save(path.join(app.config['UPLOAD_FOLDER'], uid+'.'+filetype))

def _board_addpost(uid, body, filename, filetype, ftt, board):
    alias = Board.query.filter_by(alias=board).first().alias
    pdb.session.add(
        Post(uid=uid, body=body, board_alias=alias, filename=filename, filetype=filetype, ftt=ftt)
    )

def _board_addreply(uid, body, filename, filetype, ftt, post_uid):
    pdb.session.add(
        Post(uid=uid, body=body, filename=filename, filetype=filetype, ftt=ftt)
    )

def add_super(email, password, rank):
    su = Super(uid=get_uid(), email=email, password=generate_password_hash(password), rank=rank)
    pdb.session.add(su)
    pdb.session.commit()

def confirm_application(email, rank):
    ap = Super.query.filter_by(email=email, rank=SuperTypes.APP).first()
    if ap:
        confirmed = Super(uid=ap.uid, email=email, password=ap.password, rank=rank)
        pdb.session.delete(ap)
        pdb.session.add(confirmed)
        pdb.session.commit()

def deny_application(email):
    ap = Super.query.filter_by(email=email).first()
    if ap:
        pdb.session.delete(ap)
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
