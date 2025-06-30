from blackjack_simulator.components.enums import CardSuit, CardValue

card_value_lookup = {v.value: v for v in CardValue}

_value_suit_lookup = {
    'C':CardSuit.CLUBS,
    'D':CardSuit.DIAMONDS,
    'H':CardSuit.HEARTS,
    'S':CardSuit.SPADES
}

class Card:
    def __init__(self, value:CardValue|str|int, suit:CardSuit):
        self.value = self._value_init(value)
        self.suit = self._suit_init(suit)
        # NOTE: yea didnt need suits at all for this... but would've felt weird not including them :)

    def __str__(self):
        return (f'{self.value.value}{self.suit.value}')
    
    def __repr__(self):
        return f'Card({self.value.value}, {self.suit.value})'
    
    @staticmethod
    def _value_init(value:CardValue|str|int) -> CardValue:
        ''' checks to make sure the value input for Card is ok '''
        if isinstance(value, CardValue):
            return value
        elif isinstance(value, int):
            if not value in range(2,11):
                raise ValueError(f"int value must be in range(2,11). got {value}.")
            else:
                return card_value_lookup[value]
        elif isinstance(value, str):
            if len(value) > 1:
                raise ValueError(f"str value must be in ['J', 'Q', 'K', 'A']. got {value}.")
            else:
                return card_value_lookup[value]
        else:
            raise ValueError(f"expected type (CardValue, int, str). got {type(value)}.")
            
    @staticmethod
    def _suit_init(suit:CardSuit|str) -> CardSuit:
        ''' checks to make sure suit input for Card is ok '''
        if isinstance(suit, CardSuit):
            return suit
        elif isinstance(suit, str):
            if len(suit) > 1 or suit not in ['C', 'D', 'H', 'S']:
                raise ValueError(f"str value must be in ['C', 'D', 'H', 'S']. got {suit}.")
            else:
                return _value_suit_lookup[suit]
        else:
            raise ValueError(f"expected type (CardSuit, str). got {type(suit)}.")
    
    @property
    def game_value(self) -> int: # NOTE: stupid name
        ''' int value a card represents during game. Ace = 1'''
        if self.value in [CardValue.JACK, CardValue.QUEEN, CardValue.KING]:
            return 10
        elif self.value == CardValue.ACE: # uh oh
            return 1 # will just return 1, and deal with the 11 piece in the hand code.
        else:
            return self.value.value
