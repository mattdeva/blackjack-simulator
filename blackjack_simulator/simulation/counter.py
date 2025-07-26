from __future__ import annotations

from blackjack_simulator.components.enums import CardValue
from blackjack_simulator.components.card import card_value_lookup
from blackjack_simulator.components.deck import Deck
from blackjack_simulator.components.deck import Card

ValueList = list[str|int|CardValue]

class Counter:
    ''' Helps craete and track card values to integer mapping '''
    def __init__(
        self,
        plus_list:ValueList,
        neutral_list:ValueList,
        minus_list:ValueList,
    ):
        self.plus_list = self._get_card_values(plus_list)
        self.neutral_list = self._get_card_values(neutral_list)
        self.minus_list = self._get_card_values(minus_list)

    @classmethod
    def from_low_high_cutoffs(cls, low:str|int|CardValue, high:str|int|CardValue) -> Counter:
        low,high = cls._get_card_values([low, high])

        card_values = list(CardValue)
        
        low_indx, high_indx = card_values.index(low)+1, card_values.index(high)

        plus_list = card_values[:low_indx]
        neutral_list = card_values[low_indx:high_indx]
        minus_list = card_values[high_indx:]

        return cls(plus_list, neutral_list, minus_list)
        
    @staticmethod
    def _get_card_values(input_:ValueList) -> list[CardValue]:
        out_list = []
        for i in input_:
            if isinstance(i, CardValue):
                out_list.append(i)
            else:
                out_list.append(card_value_lookup[i])
        return out_list
    
    def get_count(self, input_:Deck|list[Card]) -> int:
        count = 0
        if not isinstance(input_, Deck) and not (isinstance(input_, list) and all([isinstance(c, Card) for c in input_])):
            raise ValueError(f'must type Deck or list of Cards. got {input_}')
        
        cards = input_.drawn_cards if isinstance(input_, Deck) else input_
        
        for card in cards:
            if card.value in self.minus_list:
                count -= 1
            if card.value in self.plus_list:
                count += 1
        return count
