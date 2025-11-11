from app import app, db
from models import Deck, Card

def create_sample_data():
    with app.app_context():
        # Drop and recreate tables for sample data insertion
        db.drop_all()
        db.create_all()

        sample_decks = [
            Deck(name="Test1"),
            Deck(name="Test2"),
        ]
        db.session.add_all(sample_decks)
        db.session.commit()

        test1_deck = Deck.query.filter_by(name="Test1").first()

        sample_cards = [
            Card(deck_id=test1_deck.id, front_text="Front1",
                 back_text="Back1", order_index=1),
            Card(deck_id=test1_deck.id, front_text="Front2",
                 back_text="Back2", order_index=2),
        ]
        db.session.add_all(sample_cards)
        db.session.commit()

        print("Sample data created")


if __name__ == "__main__":
    create_sample_data()