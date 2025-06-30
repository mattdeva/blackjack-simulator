from blackjack_simulator.components.deck import Deck
from blackjack_simulator.components.enums import CardValue
from blackjack_simulator.components.card import card_value_lookup

ValueList = list[str|int|CardValue]

class CountConfig:

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
    def from_low_high_cutoffs(cls, low:str|int|CardValue, high:str|int|CardValue):
        low,high = cls._get_card_values([low, high])

        card_values = list(CardValue)
        
        low_indx, high_indx = card_values.index(low)+1, card_values.index(high)

        plus_list = card_values[:low_indx]
        neutral_list = card_values[low_indx:high_indx]
        minus_list = card_values[high_indx:]

        return cls(plus_list, neutral_list, minus_list)
        
    @staticmethod
    def _get_card_values(input_:ValueList):
        out_list = []
        for i in input_:
            if isinstance(i, CardValue):
                out_list.append(i)
            else:
                out_list.append(card_value_lookup[i])
        return out_list

# cc = CountConfig.from_low_high_cutoffs(6, 10)

# (
#     cc.minus_list,
#     cc.neutral_list,
#     cc.plus_list,
# )