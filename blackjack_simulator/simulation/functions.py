# usually dont like doing general functions script but not sure what else to do with these...
import random
from itertools import product

from blackjack_simulator.components.card import Card, CardValue, CardSuit
from blackjack_simulator.components.deck import Deck
from blackjack_simulator.simulation.count import CountConfig

def get_random_cards(n:int) -> list[Card]:
    ''' n random card creation with replacement '''
    available_cards = list(product(CardSuit, CardValue)) 
    return [Card(value, suit) for suit,value in random.choices(available_cards, k=n)]

def get_count(deck:Deck, count_config:CountConfig):
    count = 0
    for card in deck.drawn_cards:
        if card.value in count_config.minus_list:
            count -= 1
        if card.value in count_config.plus_list:
            count += 1
    return count