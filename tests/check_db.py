from app import app, db
from models import Deck, Card

with app.app_context():
    decks = Deck.query.all()
    for deck in decks:
        print(f"{deck.name} (ID: {deck.id})")

        # Query cards belonging to this deck
        cards = Card.query.filter_by(deck_id=deck.id).all()
        if cards:
            print("Cards:")
            for card in cards:
                print(f"{card.order_index} - {card.front_text} -> {card.back_text}")
        else:
            print("None")