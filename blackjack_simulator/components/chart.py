from __future__ import annotations

import pandas as pd

from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import PlayerHand
from blackjack_simulator.components.enums import Action, CardValue

_action_lookup = {v.value: v for v in Action}

_columns = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A']
_index = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
         's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', '2,2',
         '3,3', '4,4', '5,5', '6,6', '7,7', '8,8', '9,9', '10,10', 'A,A']

class Chart:
    ''' BlackJack strategy chart. Index and columns represent player hand and dealer upcard respectively. '''
    def __init__(self, df:pd.DataFrame):
        self.df = self._qc_init(df)

    @classmethod
    def from_excel(cls, path:str, sheet_name:str|bool=False) -> Chart:
        return cls(pd.read_excel(path, sheet_name=sheet_name, index_col=0))
    
    @classmethod
    def from_csv(cls, path:str) -> Chart:
        return cls(pd.read_csv(path, index_col=0))
    
    @staticmethod
    def _check_columns(df:pd.DataFrame, key:list=_columns) -> None:
        ''' check column values are correct. supposed to be rigid. '''
        if not all(df.columns == key):
            raise ValueError(f"columns must be: {key}. got {df.columns.to_list()}")
        
    @staticmethod
    def _check_index(df:pd.DataFrame, key:list=_index) -> None:
        ''' check index values are correct. supposed to be rigid. '''
        if not all(df.index == key):
            raise ValueError(f"columns must be: {key}. got {df.index.to_list()}")

    @staticmethod
    def _check_value_types(df:pd.DataFrame) -> None:
        cols_w_invalid_values = []
        for col in df:
            if not all([isinstance(i, Action) for i in df[col]]):
                cols_w_invalid_values.append(col)

        if cols_w_invalid_values:
            raise ValueError(f"found columns with invalid action values: {cols_w_invalid_values}")

    def _qc_init(self, input_df:pd.DataFrame) -> pd.DataFrame:
        ''' check to ensure attributes of table are expected. raise errors if not. '''
        # make sure column and index values are legit
        self._check_columns(input_df)
        self._check_index(input_df)

        # convert string actions to Action objects -- easier to detect if invalid value is in df
        df = input_df.replace(_action_lookup)

        # confirm the df only has Action type cell values
        self._check_value_types(df)

        return df

    # NOTE: feels like this should be structured differently and check for adequate inputs, and modularized for single responsiblily and all that jawn #10
    def action_lookup(
            self, 
            dealer_upcard_value:int|None=None, 
            dealer_upcard:Card|None=None,
            player_hand:PlayerHand|None=None, 
            player_hand_value:int|None=None
        ) -> Action:
        ''' given dealer upcard (or value) and player hand (or value) return the action based on the Chart '''
        if dealer_upcard_value is None:
            dealer_upcard_value = dealer_upcard.game_value if not dealer_upcard.value == CardValue.ACE else 'A'

        if player_hand_value is None:
            player_hand_value = player_hand.lookup_value

        action = self.df.loc[player_hand_value, dealer_upcard_value]

        return action