import pytest

from blackjack_simulator.components.card import Card
from blackjack_simulator.components.deck import Deck


def test_init():
    deck1 = Deck([Card('A','S'), Card('A','H'), Card('A','D'), Card('A','C')])
    deck2 = Deck.standard()
    deck3 = Deck.ndecks(3)
    
    assert len(deck1) == 4
    assert len(deck2) == 52
    assert len(deck3) == 156

def test_add_card():
    deck = Deck([Card('A','D'), Card('A','C')])
    deck.add_card(Card('A','S'), 'top')
    deck.add_card(Card('A','H'), 'bottom')
    deck.add_card(Card(2,'D'),1)
    
    assert deck.cards[0] == Card('A','S')
    assert deck.cards[1] == Card(2,'D')
    assert deck.cards[-1] == Card('A','H')

def test_draw():
    deck = Deck([Card('A','D'), Card('A','C')])
    deck.draw()

    assert deck.cards == [Card('A','C')]
    assert deck.drawn_cards == [Card('A','D')]