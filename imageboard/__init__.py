from flask import Flask

app = Flask(__name__)
puri = "postgresql://localhost:5432/imageboard"

class Production:
    SECRET_KEY = "TODO"
    SQLALCHEMY_DATABASE_URI = puri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
class Development:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = puri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config.from_object(Development())

# Board
from . import boards
app.register_blueprint(boards.bp)
app.add_url_rule("/", endpoint="index")

# Admins
from . import su
app.register_blueprint(su.bp)

# Click commands
from . import clickcomm as cc
cc.add_commands()
