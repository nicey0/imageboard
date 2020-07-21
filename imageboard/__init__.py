import os
from flask import Flask

app = Flask(__name__)
puri = "postgresql://localhost:5432/imageboard"

class Production:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = puri
class Development:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = puri
app.config.from_object(Production())

# Database
from . import db
db.pdb.create_all()
# db.init_app(app)

# Main
# from . import main
# app.register_blueprint(main.bp)
# app.add_url_rule("/", endpoint="index")

# Auth
# from . import auth
# app.register_blueprint(auth.bp)
