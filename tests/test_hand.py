import pytest

from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import Hand, PlayerHand, DealerHand

@pytest.mark.parametrize("cards, is_starting_hand", [
    ([Card('A','D'), Card(2,'D')],True),
    ([Card('A','D'), Card(2,'D'), Card(3,'D')],False),
])
def test_starting_hand(cards, is_starting_hand):
    assert Hand(cards).starting_hand == is_starting_hand

@pytest.mark.parametrize("cards, is_blackjack", [
    ([Card('A','D'), Card(2,'D')],False),
    ([Card(8,'D'), Card(3,'D'), Card('K','D')],False),
    ([Card('A','D'), Card('Q','D')],True),
])
def test_blackjack(cards, is_blackjack):
    assert Hand(cards).blackjack == is_blackjack

@pytest.mark.parametrize("cards, has_ace", [
    ([Card('A','D'), Card(2,'D')],True),
    ([Card(3,'D'), Card('K','D')],False),
    ([Card(8,'D'), Card('A','D'), Card('Q','D')],True),
    ([Card('A','D'), Card('A','D')],True),
])
def test_has_ace(cards, has_ace):
    assert Hand(cards).has_ace == has_ace

@pytest.mark.parametrize("cards, is_soft", [
    ([Card('A','D'), Card(2,'D'), Card(9,'D')],False),
    ([Card('K','D'), Card('A','D')],True),
    ([Card('K','D'), Card('Q','D'), Card('A','D')],False),
])
def test_starting_hand(cards, is_soft):
    assert Hand(cards).starting_hand == is_soft

@pytest.mark.parametrize("cards, total", [
    ([Card('A','D'), Card(2,'D'), Card(9,'D')],12),
    ([Card('K','D'), Card('A','D')],21),
    ([Card('K','D'), Card(6,'D'), Card(6,'D')],22),
    ([Card('K','D'), Card('Q','D'), Card('A','D')],21),
])
def test_total(cards, total):
    assert Hand(cards).total == total

@pytest.mark.parametrize("cards, is_bust", [
    ([Card('A','D'), Card(2,'D'), Card(9,'D')],False),
    ([Card('K','D'), Card(6,'D'), Card(6,'D')],True),
    ([Card('K','D'), Card(6,'D'), Card('A','D')],False),
    ([Card('K','D'), Card('Q','D'), Card('A','D')],False),
])
def test_bust(cards, is_bust):
    assert Hand(cards).bust == is_bust

@pytest.mark.parametrize("cards, add_card, error", [
    ([Card('A','D'), Card(2,'D')], Card(6,'D'), False),
    ([Card('K','D'), Card(6,'D')],(6,'D'),True),
])
def test_add_card(cards, add_card, error):
    hand = Hand(cards)
    if error:
        with pytest.raises(ValueError):
            hand.add_card(add_card)
    else:
        hand.add_card(add_card)
        assert len(hand) == 3


def test_dealer_hand_init():
    dealer_hand1 = DealerHand([Card(6,'C'), Card(7,'H')])
    dealer_hand2 = DealerHand([Card(6,'C'), Card('A','H')])

    assert len(dealer_hand1) == 2
    assert dealer_hand1.upcard == Card(7,'H')
    assert dealer_hand1.upcard_value == 7
    assert dealer_hand2.upcard_value == 'A'

@pytest.mark.parametrize("dealer_hand, is_active", [
    (DealerHand([Card('A','C'), Card(6,'H')], True), True),
    (DealerHand([Card('A','C'), Card(7,'H')], True), False),
    (DealerHand([Card('Q','C'), Card(7,'H')], True), False),
    (DealerHand([Card('A','C'), Card(6,'H')], False), False),
    (DealerHand([Card('A','C'), Card(7,'H')], False), False),
    (DealerHand([Card('Q','C'), Card(7,'H')], False), False),
])
def test_dealer_hand_active(dealer_hand, is_active):
    assert dealer_hand.active == is_active

@pytest.mark.parametrize("player_hand, is_splitable", [
    (PlayerHand([Card('A','C'), Card('A','H')]), True),
    (PlayerHand([Card('A','C'), Card('A','C')]), True),
    (PlayerHand([Card('A','C'), Card(7,'H')]), False),
    (PlayerHand([Card(3,'C'), Card(3,'H'), Card(3,'C')]), False),
])
def test_player_hand_splitable(player_hand, is_splitable):
    assert player_hand.splitable == is_splitable

@pytest.mark.parametrize("player_hand, lookup_value", [
    (PlayerHand([Card('A','C'), Card('A','H')]), 'A,A'), # splittable w Ace
    (PlayerHand([Card(3,'C'), Card(3,'H')]), '3,3'), # splittable
    (PlayerHand([Card('A','C'), Card(5,'C')]), 's16'), # soft
    (PlayerHand([Card('J','C'), Card(7,'H')]), 17), # total
    (PlayerHand([Card(3,'C'), Card(3,'H'), Card(3,'C')]), 9), # total
])
def test_player_hand_lookup_value(player_hand, lookup_value):
    assert player_hand.lookup_value == lookup_value