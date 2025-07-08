from __future__ import annotations

from dataclasses import dataclass
from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import PlayerHand
from blackjack_simulator.components.enums import Action, HandState, CardValue


@dataclass
class History:
    action: Action
    player_lookup_value: str|int
    dealer_upcard_value: str|int
    hit_card: Card|None

class Bet:
    def __init__(self, player_hand:PlayerHand, units:float=1.0, state:HandState=HandState.ACTIVE, history:list[History]|None=None):
        self.player_hand = player_hand
        self.units = units
        self.state = state
        self.history = [] if history is None else history
        
    @property
    def active(self) -> bool:
        return True if self.state == HandState.ACTIVE else False
    
    def split(self, dealer_upcard_value:CardValue) -> tuple[Bet]:
        ''' split bet into 2. add history to list. '''
        history=[History(Action.SPLIT, self.player_hand.lookup_value, dealer_upcard_value, None)]
        return (
            Bet(PlayerHand([self.player_hand.cards[0]]), self.units, history=history),
            Bet(PlayerHand([self.player_hand.cards[1]]), self.units, history=history)
        )
    
    def add_action(self, action:Action, dealer_upcard_value:CardValue, hit_card:Card|None=None) -> None:
        self.history.append(
            History(action, self.player_hand.lookup_value, dealer_upcard_value, hit_card)
        )