from . import app
from .db import Post, Board, pdb
import click
from flask.cli import with_appcontext

@click.command('init-db')
@with_appcontext
def init_db():
    pdb.drop_all()
    pdb.create_all()
    click.echo("Initialized database.")

@click.command('add-test-posts')
@with_appcontext
def add_test_posts():
    [pdb.session.delete(p) for p in Post.query.all()]
    boards = 'abcdefghijklmnopqrstuvwxyz'
    for alias in boards:
        board = Board.query.filter_by(alias=alias).first()
        for i in range(5):
            for k in range(10):
                pdb.session.add(Post(body=f"post{i}-{k}", board_alias=board.alias))
    pdb.session.commit()
    click.echo("5 pages added (10 posts each) for each board (/a/ to /z/)")

@click.command('init-boards')
@with_appcontext
def init_boards():
    [pdb.session.delete(b) for b in Board.query.all()]
    for lett in 'abcdefghijklmnopqrstuvwxyz':
        pdb.session.add(Board(alias=lett, name=lett))
    pdb.session.commit()
    click.echo("Initialized boards.")

@click.command('help')
@with_appcontext
def click_help():
    click.echo("init-db: Drops and re-initializes all database tables")
    click.echo("init-boards: Deletes and re-initializes all boards")
    click.echo("add-test-posts: Adds 5 10-post pages")

def add_commands():
    app.cli.add_command(init_db)
    app.cli.add_command(init_boards)
    app.cli.add_command(add_test_posts)
    app.cli.add_command(click_help)
