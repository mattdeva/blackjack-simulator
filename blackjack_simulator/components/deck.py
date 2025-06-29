from __future__ import annotations

import random
from itertools import product

from blackjack_simulator.components.card import Card
from blackjack_simulator.components.enums import CardSuit, CardValue

class Deck:
    def __init__(self, cards:list[Card]|None=None):
        self.cards = cards
        self.drawn_cards = [] # always set to empty list on init

    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        return f'Deck of Cards {len(self)}'
    
    def __repr__(self):
        return f'Deck of Cards {len(self)}'
    
    # NOTE: not really sure if classmethods are supposed to be used like factory methods... but im fine with it.
    @classmethod
    def standard(cls) -> Deck: # may want to init with shuffle option. for now ok.
        ''' a full deck of 52 cards '''
        return cls([Card(value, suit) for suit, value in product(CardSuit, CardValue)])
    
    @classmethod
    def ndecks(cls, n:int) -> Deck:
        return cls([Card(value, suit) for suit, value in product(CardSuit, CardValue)]*n)
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def add_card(self, card:Card, position:str|int|None) -> None:
        if isinstance(position, str):
            if position not in ['top', 'bottom', 'middle']:
                raise ValueError(f"position must be in ['top', 'bottom', 'middle']. got {position}")
            if position == 'top':
                position = 0
            if position == 'bottom':
                position = len(self)
            if position == 'middle':
                position = random.choice(range(1,len(self)))
        elif isinstance(position, int):
            if position > len(self):
                raise ValueError(f"cannot add card to position {position} in deck length {len(self)}")
        else:
            position = random.randint(1,len(self))

        self.cards.insert(card, position)

    def draw(self) -> Card:
        self.drawn_cards.append(self.cards.pop(0))
        return self.drawn_cards[-1]
