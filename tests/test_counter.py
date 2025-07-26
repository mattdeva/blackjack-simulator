import pytest 

from blackjack_simulator.components.card import Card
from blackjack_simulator.components.deck import Deck
from blackjack_simulator.components.enums import CardValue
from blackjack_simulator.simulation.counter import Counter


def test_get_card_values(): # dont need bc func called on init, but want to see example of function
    assert Counter._get_card_values([2,'K','A']) == [CardValue.TWO, CardValue.KING, CardValue.ACE]

def test_init():
    counter = Counter([2,3], [6,7], ['K','Q'])
    assert counter.plus_list == [CardValue.TWO, CardValue.THREE]
    assert counter.neutral_list == [CardValue.SIX, CardValue.SEVEN]
    assert counter.minus_list == [CardValue.KING, CardValue.QUEEN]

def test_from_low_high_cutoffs():
    counter = Counter.from_low_high_cutoffs(6,10)
    assert counter.plus_list == [CardValue.TWO, CardValue.THREE, CardValue.FOUR, CardValue.FIVE, CardValue.SIX]
    assert counter.neutral_list == [CardValue.SEVEN, CardValue.EIGHT, CardValue.NINE]
    assert counter.minus_list == [CardValue.TEN, CardValue.JACK, CardValue.QUEEN, CardValue.KING, CardValue.ACE]

@pytest.mark.parametrize("input_, output, error", [
    ([Card('K','S'), Card(8,'S'), Card(2,'S')], 0, False),
    ([Card(8,'S'), Card(2,'S')], 1, False),
    ([Card('K','S'), Card(8,'S')], -1, False),
    (Deck([Card('K','S'), Card(8,'S'), Card(2,'S')]), None, False),
    (Card('K','S'), None, True),
    (['a', 'b', Card('K','S')], None, True),

])
def test_get_count(input_, output, error):
    counter = Counter.from_low_high_cutoffs(6,10)

    if error:
        with pytest.raises(ValueError):
            counter.get_count(input_)
    else:
        if isinstance(input_, Deck):
            for i in [-1,-1,0]:
                input_.draw()
                assert counter.get_count(input_) == i
        else:
            assert counter.get_count(input_) == output