from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click
import imageboard as i

pdb = SQLAlchemy(i.app)

class Post(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    body = pdb.Column(pdb.String(10000), nullable=False)
    created = pdb.Column(pdb.DateTime)

    def __repr__(self):
        return f"<Post [{self.body[:161]}]>"

class Admin(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    email = pdb.Column(pdb.String(160))
    password = pdb.Column(pdb.String(160))

    def __repr__(self):
        return f"<Admin [{self.email}]>"

class Board(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    alias = pdb.String(1)
    name = pdb.String(160)

    def __repr__(self):
        return f"<Board [{self.name}]>"

@click.command('init-db')
@with_appcontext
def init_db_command():
    pdb.drop_all()
    pdb.create_all()
    click.echo("Initialized database.")

def init_app(app):
    # Add init-db command to click
    app.cli.add_command(init_db_command)
