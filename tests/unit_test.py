import pytest
from flask import session
from app import app, db
from models import Deck, Card

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    app.config['SECRET_KEY'] = "test"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def create_deck_with_cards():
    deck = Deck(name="Unit Test Deck")
    db.session.add(deck)
    db.session.commit()

    cards = []
    for i in range(1, 4):
        card = Card(
            deck_id=deck.id,
            front_text=f"front{i}",
            back_text=f"back{i}",
            order_index=i
        )
        cards.append(card)
        db.session.add(card)
    
    db.session.commit()
    return deck, cards


def test_study_shuffle_persists(client):
    # Create test deck + cards
    deck, cards = create_deck_with_cards()

    # First request
    res = client.get(f"/deck/{deck.id}/study?shuffle=true")
    assert res.status_code == 200

    with client.session_transaction() as sess:
        assert "study_order" in sess
        order_at_start = list(sess["study_order"])


    # Second request
    res2 = client.get(f"/deck/{deck.id}/study?shuffle=true&index=1")
    assert res2.status_code == 200

    with client.session_transaction() as sess:
        assert sess["study_order"] == order_at_start


    # Third request
    res3 = client.get(f"/deck/{deck.id}/study?shuffle=true&index=2")
    assert res3.status_code == 200

    with client.session_transaction() as sess:
        assert sess["study_order"] == order_at_start