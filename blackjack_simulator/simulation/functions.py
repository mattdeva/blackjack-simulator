# usually dont like doing general functions script but not sure what else to do with these...
import random
from itertools import product

from blackjack_simulator.components.card import Card, CardValue, CardSuit
from blackjack_simulator.simulation.counter import Counter

def get_random_cards(n:int) -> list[Card]: # not used outside of testing things
    ''' n random card creation with replacement '''
    available_cards = list(product(CardSuit, CardValue)) 
    return [Card(value, suit) for suit,value in random.choices(available_cards, k=n)]

def get_count(cards:list[Card], counter:Counter):
    # NOTE: after writing tests im thinking this should be counter method...
    # ...but doesnt matter too much and dont want to leave a function alone in this script :)
    count = 0
    for card in cards:
        if card.value in counter.minus_list:
            count -= 1
        if card.value in counter.plus_list:
            count += 1
    return count