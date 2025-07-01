# usually dont like doing general functions script but not sure what else to do with these...
import random
from itertools import product

from blackjack_simulator.components.card import Card, CardValue, CardSuit
from blackjack_simulator.components.deck import Deck
from blackjack_simulator.simulation.counter import Counter

def get_random_cards(n:int) -> list[Card]:
    ''' n random card creation with replacement '''
    available_cards = list(product(CardSuit, CardValue)) 
    return [Card(value, suit) for suit,value in random.choices(available_cards, k=n)]

def get_count(deck:Deck, counter:Counter):
    count = 0
    for card in deck.drawn_cards:
        if card.value in counter.minus_list:
            count -= 1
        if card.value in counter.plus_list:
            count += 1
    return count