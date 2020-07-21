from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from datetime import datetime as dt
import click
import imageboard as i

pdb = SQLAlchemy(i.app)

class Post(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    title = pdb.Column(pdb.String(2000), unique=True, nullable=False)
    body = pdb.Column(pdb.String(10000))
    created = pdb.Column(pdb.DateTime(default=dt.utcnow))

    def __repr__(self):
        return f"<Post [{self.title[:161]}]>"

class Admin(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    email = pdb.Column(pdb.String(160))
    password = pdb.Column(pdb.String(160))

    def __repr__(self):
        return f"<Admin [{self.email}]>"

def init_db():
    pdb.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized database.")

def init_app(app):
    # Add init-db command to click
    app.cli.add_command(init_db_command)
