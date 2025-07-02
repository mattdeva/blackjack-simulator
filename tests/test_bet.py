from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import PlayerHand
from blackjack_simulator.components.bet import Bet
from blackjack_simulator.components.enums import HandState, Action

def test_init():
    bet = Bet(PlayerHand([Card('K','D'), Card(3,'S')]))
    assert bet.units == 1
    assert bet.state == HandState.ACTIVE
    assert bet.history == []
    assert bet.active == True

def test_active():
    bet = Bet(PlayerHand([Card('K','D'), Card(3,'S')]))

    for state in [HandState.BLACKJACK, HandState.BUST, HandState.DOUBLE, HandState.OOF, HandState.STAND, HandState.SURRENDER]:
        bet.state = state
        assert bet.active == False

def test_add_action():
    bet = Bet(PlayerHand([Card('K','D'), Card(3,'S')]))
    bet.add_action(Action.HIT, 7)
    assert len(bet.history) == 1

def test_split():
    bet = Bet(PlayerHand([Card(3,'D'), Card(3,'S')]))
    split1, split2 = bet.split(5)
    
    assert len(split1.history)== len(split2.history) == 1
    assert split1.units == split2.units == 1
    assert split1.history[0] == split2.history[0] == (Action.SPLIT, '3,3', 5)