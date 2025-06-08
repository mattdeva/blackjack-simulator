from __future__ import annotations

import pandas as pd

from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import PlayerHand
from blackjack_simulator.components.enums import Action, CardValue

_action_lookup = {v.value: v for v in Action}

class Chart:
    def __init__(self, df:pd.DataFrame):
        self.df = self._qc_init(df)

    @classmethod
    def from_excel(cls, path:str, sheet_name:str|bool=False) -> Chart:
        return cls(pd.read_excel(path, sheet_name=sheet_name, index_col=0))
    
    @classmethod
    def from_csv(cls, path:str) -> Chart:
        return cls(pd.read_csv(path, index_col=0))
    
    @staticmethod
    def _qc_init(input_df:pd.DataFrame) -> pd.DatFrame:

        # make sure column values are legit (these should maybe be enums too?)
        if not all(input_df.columns == [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A']):
            raise ValueError(f"columns must be: [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A']. got {input_df.columns.to_list()}")
        
        # TODO: eventually do the same with index

        # convert string actions to Action objects -- easier to detect if invalid value is in df
        df = input_df.replace(_action_lookup)

        cols_w_invalid_values = []
        for col in df:
            if not all([isinstance(i, Action) for i in df[col]]):
                cols_w_invalid_values.append(col)

        if cols_w_invalid_values:
            raise ValueError(f"found columns with invalid action values: {cols_w_invalid_values}")

        return df

    # NOTE: should split this function up.. checking for adequate inputs, and single responsiblily and all that jawn
    def action_lookup(
            self, 
            dealer_upcard_value:int|None=None, 
            dealer_upcard:Card|None=None,
            player_hand:PlayerHand|None=None, 
            player_hand_value:int|None=None
        ):
        if dealer_upcard_value is None:
            dealer_upcard_value = dealer_upcard.game_value if not dealer_upcard.value == CardValue.ACE else 'A'

        if player_hand_value is None:
            player_hand_value = player_hand.lookup_value

        action_str = self.df.loc[player_hand_value, dealer_upcard_value]

        return action_str