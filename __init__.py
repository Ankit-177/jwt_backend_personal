from flask import Flask
# from flask_cors import CORS # Error #1: ImportError: cannot import name 'cors' from '__init__' (/home/ankitp/vscode/jwt_backend_personal/__init__.py)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

"""
These imports define the key objects
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
These object and definitions are used throughout the Jupyter Notebook.
"""

# Setup of key Flask object (app)
app = Flask(__name__)
# Setup SQLAlchemy object and properties for the database (db)
database = 'sqlite:///sqlite.db'  # path and filename of database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy()
Migrate(app, db)

# This belongs in place where it runs once per project
db.init_app(app)

# Images storage
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # supported file types
app.config['UPLOAD_FOLDER'] = 'volumes/uploads/'  # location of user uploaded content
