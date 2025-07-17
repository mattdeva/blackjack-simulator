import pytest
import pandas as pd

from blackjack_simulator.components.enums import Action
from blackjack_simulator.components.chart import Chart
from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import PlayerHand

@pytest.fixture
def chart():
    return Chart.from_excel('data/strategy_charts.xlsx', sheet_name='Chart1')

@pytest.mark.parametrize("df, key, error", [
    (pd.DataFrame({'a':[1,2], 'b':[3,4]}), ['a','b'], False),
    (pd.DataFrame({'a':[1,2], 'b':[3,4]}), ['a','c'],  True), 
])
def test_check_columns(df, key, error):
    if error:
        with pytest.raises(ValueError):
            Chart._check_columns(df, key)
    else:
        Chart._check_columns(df, key)

@pytest.mark.parametrize("df, key, error", [
    (pd.DataFrame({'a':[1,2], 'b':[3,4]}), [0,1], False),
    (pd.DataFrame({'a':[1,2], 'b':[3,4]}), [1,2],  True), 
])
def test_check_index(df, key, error):
    if error:
        with pytest.raises(ValueError):
            Chart._check_index(df, key)
    else:
        Chart._check_index(df, key)

@pytest.mark.parametrize("df, error", [
    (pd.DataFrame({'a':[1,2], 'b':[3,4]}), True),
    (pd.DataFrame({'a':[1,2], 'b':[Action.HIT,Action.DOUBLE]}), True), 
    (pd.DataFrame({'a':[Action.STAND,Action.SPLIT], 'b':[Action.HIT,Action.DOUBLE]}), False), 
])
def test_check_value_types(df, error):
    if error:
        with pytest.raises(ValueError):
            Chart._check_value_types(df)
    else:
        Chart._check_value_types(df)


@pytest.mark.parametrize("dealer_upcard_value, dealer_upcard, player_hand, player_hand_value", [
    ('A', None, None, 10),
    (None, Card('A','D'), PlayerHand([Card(5,'H'), Card(5,'S')]), None),
    (10, None, PlayerHand([Card(5,'H'), Card(5,'S')]), None),
    (10, None, None, 10),
])
def test_action_lookup(dealer_upcard_value, dealer_upcard, player_hand, player_hand_value, chart):
    assert isinstance(
        chart.action_lookup(dealer_upcard_value, dealer_upcard, player_hand, player_hand_value), 
        Action
    )