import pytest

from blackjack_simulator.components.enums import HandState
from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import DealerHand, PlayerHand
from blackjack_simulator.components.bet import Bet
from blackjack_simulator.simulation.game import calculate_payout

@pytest.mark.parametrize("bet, dealer_hand, payout", [
    (Bet(PlayerHand([Card('A','S'), Card('J','S')]), state=HandState.BLACKJACK), DealerHand([Card(3,'H'), Card(5,'C')]), 2.5), # blackjack
    (Bet(PlayerHand([Card('A','S'), Card('J','S')]), state=HandState.BLACKJACK), DealerHand([Card('A','H'), Card(10,'D')]), 1), # blackjack push
    (Bet(PlayerHand([Card(6,'S'), Card('J','S')]), state=HandState.SURRENDER), DealerHand([Card('A','H'), Card(9,'D')]), .5), # surrender
    (Bet(PlayerHand([Card(7,'S'), Card('J','S')])), DealerHand([Card('K','H'), Card(6,'D'), Card(7,'S')]), 2), # dealter bust
    (Bet(PlayerHand([Card(7,'S'), Card('J','S')]), state=HandState.DOUBLE), DealerHand([Card('K','H'), Card(6,'D'), Card(7,'S')]), 2), # dealter bust + double
    (Bet(PlayerHand([Card(9,'S'), Card('J','S')])), DealerHand([Card('A','H'), Card(7,'D')]), 2), # player total >
    (Bet(PlayerHand([Card(9,'S'), Card('J','S')]), state=HandState.DOUBLE), DealerHand([Card('A','H'), Card(7,'D')]), 2), # player total > + double
    (Bet(PlayerHand([Card(9,'S'), Card('J','S')])), DealerHand([Card('A','H'), Card(9,'D')]), 0), # dealer total >
    (Bet(PlayerHand([Card(8,'S'), Card('J','S')])), DealerHand([Card('A','H'), Card(7,'D')]), 1), # push
])
def test_calculate_payout(bet, dealer_hand, payout):
    assert calculate_payout(bet, dealer_hand, 1.5, .5) == payout