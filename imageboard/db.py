from flask_sqlalchemy import SQLAlchemy
import imageboard as i

pdb = SQLAlchemy(i.app)
pdb.init_app(i.app)

class Admin(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True, nullable=False)
    email = pdb.Column(pdb.String(160), nullable=False)
    password = pdb.Column(pdb.String(160), nullable=False)

    def __repr__(self):
        return f"<Admin [{self.email}]>"

class Board(pdb.Model):
    alias = pdb.Column(pdb.String(1), primary_key=True, nullable=False)
    name = pdb.Column(pdb.String(160), nullable=False)
    posts = pdb.relationship("Post", backref="board", lazy=True)

    def __repr__(self):
        return f"<Board [{self.name} | {len(self.posts)}]>"

class Post(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True, nullable=False)
    body = pdb.Column(pdb.String(10000), nullable=False)
    board_alias = pdb.Column(pdb.String(1), pdb.ForeignKey('board.alias'), nullable=False)

    def __repr__(self):
        return f"<Post [/{self.board_alias}/ | {self.body[:80]}]>"
