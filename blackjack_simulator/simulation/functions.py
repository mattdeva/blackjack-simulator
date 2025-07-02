# usually dont like doing general functions script but not sure what else to do with these...
import random
from itertools import product

from blackjack_simulator.components.deck import Deck
from blackjack_simulator.components.card import Card, CardValue, CardSuit
from blackjack_simulator.components.hand import PlayerHand, DealerHand
from blackjack_simulator.simulation.counter import Counter

def get_random_cards(n:int) -> list[Card]: # not used outside of testing things
    ''' n random card creation with replacement '''
    available_cards = list(product(CardSuit, CardValue)) 
    return [Card(value, suit) for suit,value in random.choices(available_cards, k=n)]

def get_count(cards:list[Card], counter:Counter):
    # NOTE: after writing tests im thinking this should be counter method...but doesnt matter too much
    count = 0
    for card in cards:
        if card.value in counter.minus_list:
            count -= 1
        if card.value in counter.plus_list:
            count += 1
    return count

def deal(deck:Deck) -> tuple[PlayerHand, DealerHand]:
    ''' deal a single player_hand and a dealer_hand '''
    player_cards = []
    dealer_cards = []

    player_cards.append(deck.draw())
    dealer_cards.append(deck.draw())
    player_cards.append(deck.draw())
    dealer_cards.append(deck.draw())

    return PlayerHand(player_cards), DealerHand(dealer_cards)

def shuffle_cut_deck(n_decks:int) -> tuple[Deck, int]:
    deck = Deck.ndecks(n_decks)
    deck.shuffle()

    # cut card / stop value will be somewhere in the middle half of the deck
    stop = random.randint(
        int(len(deck)*.25),
        int(len(deck)*.75),
    )

    return deck, stop
