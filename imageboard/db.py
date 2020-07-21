from flask_sqlalchemy import SQLAlchemy
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
