from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config
import random

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import Deck, Card

# Helper functions
def get_deck(deck_id):
    deck = db.session.get(Deck, deck_id)
    if deck is None:
        abort(404)
    return deck

def get_card(card_id):
    card = db.session.get(Card, card_id)
    if card is None:
        abort(404)
    return card

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
        db.session.commit()
        return redirect(url_for('deck_detail', deck_id=new_deck.id))
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

# Study mode
@app.route('/deck/<int:deck_id>/study', methods=['GET', 'POST'])
def study_deck(deck_id):
    deck = get_deck(deck_id)
    shuffle_toggle = request.args.get('shuffle', None)
    current_index = int(request.args.get('index', 0))
    show_back = request.args.get('show', 'false').lower() == 'true'

    if 'study_order' not in session or session.get('deck_id') != deck_id:
        order_ids = [card.id for card in deck.cards]
        session['study_order'] = order_ids
        session['deck_id'] = deck_id
        session['shuffle_enabled'] = False

    if shuffle_toggle is not None:
        shuffle_enabled = shuffle_toggle.lower() == 'true'
        if shuffle_enabled != session.get('shuffle_enabled', False):
            order_ids = [card.id for card in deck.cards]
            if shuffle_enabled:
                random.shuffle(order_ids)
            session['study_order'] = order_ids
            session['shuffle_enabled'] = shuffle_enabled

    order_ids = session['study_order']
    shuffle_enabled = session.get('shuffle_enabled', False)

    if current_index >= len(order_ids):
        return render_template('study_complete.html', deck=deck, shuffle_enabled=shuffle_enabled)

    card_id = order_ids[current_index]
    card = get_card(card_id)

    return render_template(
        'study.html',
        deck=deck,
        card=card,
        current_index=current_index,
        total=len(order_ids),
        show_back=show_back,
        shuffle_enabled=shuffle_enabled
    )
