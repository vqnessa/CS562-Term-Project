from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import Deck, Card

# Helper functions
def get_deck(deck_id):
    return Deck.query.get_or_404(deck_id)

def get_card(card_id):
    return Card.query.get_or_404(card_id)

def commit_and_redirect(endpoint, **values):
    db.session.commit()
    return redirect(url_for(endpoint, **values))

# Deck
@app.route('/')
def index():
    decks = Deck.query.order_by(Deck.created_at.desc()).all()
    return render_template('homepage.html', decks=decks)

@app.route('/deck/new', methods=['GET', 'POST'])
def create_deck():
    if request.method == 'POST':
        new_deck = Deck(name=request.form['name'])
        db.session.add(new_deck)
        return commit_and_redirect('index')
    return render_template('deck_form.html')

@app.route('/deck/<int:deck_id>/edit', methods=['GET', 'POST'])
def edit_deck(deck_id):
    deck = get_deck(deck_id)
    if request.method == 'POST':
        deck.name = request.form['name']
        return commit_and_redirect('index')
    return render_template('deck_form.html', deck=deck)

@app.route('/deck/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    db.session.delete(get_deck(deck_id))
    return commit_and_redirect('index')

@app.route('/deck/<int:deck_id>')
def deck_detail(deck_id):
    deck = get_deck(deck_id)
    return render_template('deck_detail.html', deck=deck)

# Card
@app.route('/deck/<int:deck_id>/card/new', methods=['GET', 'POST'])
def create_card(deck_id):
    deck = get_deck(deck_id)
    if request.method == 'POST':
        new_card = Card(
            deck_id=deck.id,
            front_text=request.form['front_text'],
            back_text=request.form['back_text'],
            order_index=request.form.get('order_index', 0)
        )
        db.session.add(new_card)
        return commit_and_redirect('deck_detail', deck_id=deck.id)
    return render_template('card_form.html', deck=deck)

@app.route('/deck/<int:deck_id>/card/<int:card_id>/edit', methods=['GET', 'POST'])
def edit_card(deck_id, card_id):
    deck = get_deck(deck_id)
    card = get_card(card_id)
    if request.method == 'POST':
        card.front_text = request.form['front_text']
        card.back_text = request.form['back_text']
        card.order_index = request.form.get('order_index', 0)
        return commit_and_redirect('deck_detail', deck_id=deck.id)
    return render_template('card_form.html', deck=deck, card=card)

@app.route('/deck/<int:deck_id>/card/<int:card_id>/delete', methods=['POST'])
def delete_card(deck_id, card_id):
    db.session.delete(get_card(card_id))
    return commit_and_redirect('deck_detail', deck_id=deck_id)