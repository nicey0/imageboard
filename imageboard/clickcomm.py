from . import app
from .db import Post, Board, pdb
import click
from flask.cli import with_appcontext

@click.command('init-db')
@with_appcontext
def init_db_command():
    pdb.drop_all()
    pdb.create_all()
    click.echo("Initialized database.")

@click.command('add-test-posts')
@with_appcontext
def add_test_posts():
    [pdb.session.delete(p) for p in Post.query.all()]
    for i in range(5):
        for k in range(10):
            pdb.session.add(Post(body=f"post{i}-{k}"))
    pdb.session.commit()
    click.echo("5 pages added (10 posts each)")

@click.command('init-boards')
@with_appcontext
def init_boards():
    for lett in 'abcdefghijklmnopqrstuvwxyz':
        pdb.session.add(Board(alias=lett, name=lett))
    pdb.session.commit()
    click.echo("Initialized boards.")

def add_commands():
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_test_posts)
    app.cli.add_command(init_boards)
