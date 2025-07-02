from __future__ import annotations

from blackjack_simulator.components.hand import PlayerHand
from blackjack_simulator.components.enums import Action, HandState, CardValue

class Bet:
    def __init__(self, player_hand:PlayerHand, units:float=1.0, state:HandState=HandState.ACTIVE, history:list|None=None):
        self.player_hand = player_hand
        self.units = units
        self.state = state
        self.history = [] if history is None else history
        # NOTE: should make a custom object for this (can do later)
        
    @property
    def active(self):
        return True if self.state == HandState.ACTIVE else False
    
    def split(self, dealer_upcard_value:CardValue) -> tuple[Bet]:
        ''' split bet into 2. add history to list. '''
        history=[(Action.SPLIT, self.player_hand.lookup_value, dealer_upcard_value)]
        return (
            Bet(PlayerHand([self.player_hand.cards[0]]), self.units, history=history),
            Bet(PlayerHand([self.player_hand.cards[1]]), self.units, history=history)
        )
    
    def add_action(self, action:Action, dealer_upcard_value:CardValue):
        self.history.append((action, self.player_hand.lookup_value, dealer_upcard_value))