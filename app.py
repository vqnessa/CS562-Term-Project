from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import Deck, Card

@app.route('/')
def index():
    decks = Deck.query.order_by(Deck.created_at.desc()).all()
    return render_template('homepage.html', decks=decks)

@app.route('/deck/new', methods=['GET', 'POST'])
def create_deck():
    if request.method == 'POST':
        name = request.form['name']
        new_deck = Deck(name=name)
        db.session.add(new_deck)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('deck_form.html')

@app.route('/deck/<int:deck_id>/edit', methods=['GET', 'POST'])
def edit_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if request.method == 'POST':
        deck.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('deck_form.html', deck=deck)

@app.route('/deck/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    db.session.delete(deck)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/deck/<int:deck_id>')
def deck_detail(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    return render_template('deck_detail.html', deck=deck)