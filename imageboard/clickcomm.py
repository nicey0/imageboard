from . import app
from .db import pdb, SuperTypes, Super, Board, Post
from .util import board_addpost, clear_post_files
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

@click.command('init-db')
@with_appcontext
def init_db():
    pdb.drop_all()
    pdb.create_all()
    clear_post_files()
    click.echo("Initialized database.")

@click.command('init-admin')
@click.argument('email', nargs=1)
@click.argument('password', nargs=1)
@with_appcontext
def init_admin(email, password):
    pdb.session.add(Super(email=email, password=generate_password_hash(password),
                          rank=SuperTypes.ADM))
    pdb.session.commit()
    click.echo("Superadmin initialized")

@click.command('init-boards')
@with_appcontext
def init_boards():
    for lett in 'abcdefghijklmnopqrstuvwxyz':
        pdb.session.add(Board(alias=lett, name=lett))
    pdb.session.commit()
    click.echo("Initialized boards.")

def add_commands():
    app.cli.add_command(init_db)
    app.cli.add_command(init_admin)
    app.cli.add_command(init_boards)
