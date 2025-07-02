import random
import pandas as pd
from itertools import product

from blackjack_simulator.components.chart import Chart
from blackjack_simulator.components.bet import Bet
from blackjack_simulator.simulation.functions import deal, shuffle_cut_deck
from blackjack_simulator.simulation.game import run_dealer_actions, run_player_actions, calculate_payout

from typing import Sequence


def summarize(sequence:Sequence[tuple[float]]) -> dict[str, float]:
    #     tuples = [
    #     (1,0),
    #     (1,2),
    #     (1,1.5),
    #     (2,0),
    #     (2,4),
    #     (1,0)
    # ] -> {'total_buyin': 8, 'total_payout': 7.5, 'total_obs': 6}
    total_buyin = sum([t[0] for t in sequence])
    total_payout = sum([t[1] for t in sequence])
    return {
        'total_buyin' : total_buyin,
        'total_payout' : total_payout,
        'total_obs' : len(sequence),
        'roi':round(total_payout/total_buyin*100,1) if len(sequence) > 0 else 'N/A'
    }

def result_dict_to_df(results_dict:dict, metric='roi'):
    metric_dict = {k:v[metric] for k,v in results_dict.items()}
    df = pd.DataFrame.from_dict(metric_dict, orient='index').reset_index()

    # split index column into rows, columns
    df[['player_hand', 'columns']] = pd.DataFrame(df['index'].tolist(), index=df.index)

    # remove index column
    df = df.drop('index', axis=1)

    # pivot
    df = df.pivot(index='player_hand', columns='columns', values=0).reset_index()

    # stupid
    df.columns.name = ''

    return df

class Simulator:
    def __init__(
            self,
            chart:Chart, # TODO: add flexible charts in future
            dealer_hit_soft_17:bool = True,
            n_decks: int = 6,
            max_splits:int = 4,
            blackjack_payout:float = 3/2,
            surrender_payout:float = 1/2
        ):
        self.chart = chart
        self.dealer_hit_soft_17 = dealer_hit_soft_17
        self.n_decks = n_decks
        self.max_splits = max_splits
        self.blackjack_payout = blackjack_payout
        self.surrender_payout = surrender_payout
        
        # TEMP -- fix to update several strategies based on deck hotness
        self._results_dict = None

    @staticmethod
    def _track_results(results_dict:dict, bet:Bet, payout:float) -> None:
        # NOTE: in future may want to track how win/loss happened (bust/showdown) (prob would have to change game a lil)
        for action in bet.history:
            results_dict[(action[1], action[2])].append((bet.units, payout))

    @staticmethod
    def _get_empty_results(chart:Chart):
        results_dict = {}
        hand_combos =  list(product(chart.df.index.to_list(), chart.df.columns.to_list()))
        for hand_combo in hand_combos:
            results_dict[hand_combo] = []
        return results_dict
    
    def result_dict_to_df(self, metric='roi') -> pd.DataFrame:

        # NOTE: think this will error if try to run without running simulation... should fix that.

        metric_dict = {k:v[metric] for k,v in self.results_dict.items()}
        df = pd.DataFrame.from_dict(metric_dict, orient='index').reset_index()

        # split index column into rows, columns
        df[['player_hand', 'columns']] = pd.DataFrame(df['index'].tolist(), index=df.index)

        # remove index column
        df = df.drop('index', axis=1)

        # pivot
        df = df.pivot(index='player_hand', columns='columns', values=0).reset_index()

        # stupid
        df.columns.name = ''

        return df
    
    @property
    def results_dict(self) -> dict:
        if self._results_dict is None:
            self._results_dict = self._get_empty_results(self.chart) # NOTE: would need to be updated if using multiple charts
        return self._results_dict


    def run(self, hands = 10, overwrite:bool=False) -> None:

        if self._results_dict is not None and not overwrite:
            raise ValueError(f'non-emtpy results. must set overwrite to True') # safeguard agaisnt overwriting (temp prob)
                
        deck, stop= shuffle_cut_deck(self.n_decks)
        hand_counter = 0
        shoe_counter = 0
        
        while hand_counter < hands:
            if shoe_counter > stop:
                deck,stop = shuffle_cut_deck(self.n_decks)
            start_n_cards = len(deck) # lazy way to get how many cards used per round...
            player_hand, dealer_hand = deal(deck)

            bet = Bet(player_hand, units=1) # TODO: flexible units involving pressing & deck cound
            bets = run_player_actions(bet , dealer_hand, deck, self.chart)
            run_dealer_actions(dealer_hand, bets, deck)

            for bet in bets:
                payout = calculate_payout(bet, dealer_hand, self.blackjack_payout, self.surrender_payout)
                self._track_results(self.results_dict, bet, payout)

            end_n_cards = len(deck)
            shoe_counter += start_n_cards - end_n_cards

            hand_counter +=1
        self._results_dict = {k:summarize(v) for k,v in self._results_dict.items()}
