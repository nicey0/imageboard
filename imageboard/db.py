from flask_sqlalchemy import SQLAlchemy
from . import app

pdb = SQLAlchemy(app)

class Post(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    title = pdb.Column(pdb.String(2000), unique=True, nullable=False)
    body = pdb.Column(pdb.String(10000))
    dt = pdb.Column(pdb.DateTime())

    def __repr__(self):
        return f"<Post [{self.title[:161]}]>"

class Admin(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    email = pdb.Column(pdb.String(160))
    password = pdb.Column(pdb.String(160))

    def __repr__(self):
        return f"<Admin [{self.email}]>"
