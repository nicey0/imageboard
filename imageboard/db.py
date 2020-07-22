from flask_sqlalchemy import SQLAlchemy
import imageboard as i

pdb = SQLAlchemy(i.app)

class Admin(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    email = pdb.Column(pdb.String(160))
    password = pdb.Column(pdb.String(160))

    def __repr__(self):
        return f"<Admin [{self.email}]>"

class Board(pdb.Model):
    alias = pdb.Column(pdb.String(1), primary_key=True)
    name = pdb.Column(pdb.String(160))
    posts = pdb.relationship("Post", backref="board", lazy=True)

    def __repr__(self):
        return f"<Board [{self.name}]>"

class Post(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True)
    body = pdb.Column(pdb.String(10000), nullable=False)
    board_alias = pdb.Column(pdb.String(1), pdb.ForeignKey('board.alias'))
    # board = pdb.relationship('Board')

    def __repr__(self):
        return f"<Post {self.body[:80]}>"
        # return f"<Post [{self.board_alias} | {self.body[:80]}]>"
