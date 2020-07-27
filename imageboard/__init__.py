from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
puri = "postgresql://localhost:5432/imageboard"
upload = 'imageboard/static/POSTS/'
class Production:
    SECRET_KEY = "TODO"
    SQLALCHEMY_DATABASE_URI = puri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = upload + 'PRODUCTION'
class Development:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = puri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = upload + 'DEVELOPMENT'
app.config.from_object(Development())
limiter = Limiter(app, key_func=get_remote_address)

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
