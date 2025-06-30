import pytest

from blackjack_simulator.components.enums import CardSuit, CardValue
from blackjack_simulator.components.card import Card


def test_attributes():
    card = Card(2,'D')
    assert card.value == CardValue.TWO
    assert card.suit == CardSuit.DIAMONDS

@pytest.mark.parametrize("value, suit, error", [
    (3,'C',False),
    ('J','S',False),
    (CardValue.KING,CardSuit.HEARTS,False), # i prob should iterate over every possible combo but this is fine sample
    ('A','Y',True), # no Y suit
    (1,'H',True), # no 1 value
    (2.0,'H',True), # no floats
    ('10','H',True), # number cards need int input
    ('P','S',True) # no P value
])
def test_card_init(value, suit, error):
    if error:
        with pytest.raises((ValueError, KeyError)):
            Card(value, suit)
    else:
        assert isinstance(Card(value, suit), Card)

@pytest.mark.parametrize("card_value, game_value", [
    (5,5),
    ('J',10),
    ('A',1)
])
def test_game_value(card_value, game_value):
    assert Card(card_value, 'D').game_value == game_value