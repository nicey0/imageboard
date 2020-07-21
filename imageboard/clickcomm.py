from . import app
from .db import Post, Board, pdb
import click
from flask.cli import with_appcontext

@click.command('add-test-posts')
@with_appcontext
def add_test_posts():
    for i in range(5):
        pdb.session.add(Post(body=f"post{i}"))
    click.echo("5 posts added")

@click.command('init-boards')
@with_appcontext
def init_boards():
    for lett in 'abcdefghijklmnopqrstuvwxyz':
        pdb.session.add(Board(alias=lett, name=lett))
    pdb.session.commit()
    click.echo("Initialized boards.")

def add_command():
    app.cli.add_command(add_test_posts)
    app.cli.add_command(init_boards)
