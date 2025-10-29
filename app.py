from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from models import Deck, Card

# Initialize database
with app.app_context():
    db.create_all()
    print("Database initialized.")