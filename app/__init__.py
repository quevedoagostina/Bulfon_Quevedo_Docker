import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

db = SQLAlchemy(app)
