from flask_sqlalchemy import SQLAlchemy
import imageboard as i
from enum import Enum
# utcnow ------
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
# utcnow ------

pdb = SQLAlchemy(i.app)
pdb.init_app(i.app)

# utcnow()
class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

@compiles(utcnow, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"

# Models
class AdminTypes(Enum):
    ADMIN = 0
    MOD = 1
class Admin(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True, nullable=False)
    email = pdb.Column(pdb.String(160), nullable=False)
    password = pdb.Column(pdb.String(160), nullable=False)
    rank = pdb.Column(pdb.Enum(AdminTypes))

    def __repr__(self):
        return f"<Admin [{self.uid} | {self.email}]>"

class Board(pdb.Model):
    alias = pdb.Column(pdb.String(1), primary_key=True, nullable=False)
    name = pdb.Column(pdb.String(160), nullable=False)
    posts = pdb.relationship("Post", backref="board", lazy=True)

    def __repr__(self):
        return f"<Board [{self.alias}/{self.name} | {len(self.posts)}]>"

class Post(pdb.Model):
    uid = pdb.Column(pdb.Integer, primary_key=True, nullable=False)
    body = pdb.Column(pdb.String(10000), nullable=False)
    board_alias = pdb.Column(pdb.String(1), pdb.ForeignKey('board.alias'), nullable=False)
    created = pdb.Column(pdb.DateTime, server_default=utcnow())

    def __repr__(self):
        return f"<Post [/{self.board_alias}/ | {self.created} | {self.body[:50]}]>"
