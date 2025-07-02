from blackjack_simulator.components.card import Card
from blackjack_simulator.components.deck import Deck
from blackjack_simulator.components.hand import PlayerHand, DealerHand
from blackjack_simulator.simulation.counter import Counter
from blackjack_simulator.simulation.functions import (
    get_random_cards, get_count, deal, shuffle_cut_deck
)

def test_get_random_cards():
    two_random_cards = get_random_cards(2)
    three_random_cards = get_random_cards(2)

    assert len(two_random_cards) == 2
    assert len(three_random_cards) == 2
    assert all([True if isinstance(c, Card) else False for c in two_random_cards])
    assert all([True if isinstance(c, Card) else False for c in three_random_cards])

def test_get_count():
    cards = [Card('K','S'), Card(8,'S'), Card(2,'S')]
    counter = Counter.from_low_high_cutoffs(6,10)

    assert get_count(cards, counter) == 0
    assert get_count(cards[1:], counter) == 1
    assert get_count(cards[:-1], counter) == -1

def test_deal():
    deck = Deck.standard()
    player_hand, dealer_hand = deal(deck)

    assert len(player_hand.cards) == len(dealer_hand) == 2
    assert isinstance(player_hand, PlayerHand)
    assert isinstance(dealer_hand, DealerHand)
    assert len(deck) == 48

def test_shuffle_cut_deck():
    deck,stop = shuffle_cut_deck(3)
    
    assert len(deck)==156
    assert isinstance(deck, Deck)
    assert isinstance(stop, int)
