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
