import pandas as pd
from itertools import product
from dataclasses import dataclass

from blackjack_simulator.components.chart import Chart
from blackjack_simulator.components.bet import Bet
from blackjack_simulator.components.card import Card
from blackjack_simulator.components.enums import Action
from blackjack_simulator.simulation.counter import Counter
from blackjack_simulator.simulation.functions import deal, shuffle_cut_deck, get_count
from blackjack_simulator.simulation.game import run_dealer_actions, run_player_actions, calculate_payout

from typing import Sequence


@dataclass
class Record:
    ''' Way to record and hands, situations, and results '''
    hand_id: str
    player_hand_lookup: str|int
    dealer_upcard_value: str|int
    count: int
    chart: int
    bet_units: float
    action: Action
    hit_card: Card
    final_payout: float 

    @property
    def result(self) -> int:
        return 1 if self.final_payout > self.bet_units else 0 if self.final_payout == self.bet_units else -1
    
    @property
    def chart_lookup(self) -> tuple[str]:
        return (self.player_hand_lookup, self.dealer_upcard_value)
    
    def to_dict(self) -> dict:
        d = self.__dict__
        d.update({'result':self.result})
        return d

def get_hand_id(x: int, digits: int) -> str:
    if x < 0:
        raise ValueError("Input must be a positive integer.")
    return str(x).zfill(digits)

def summarize_str_to_dict(str_:str) -> dict[str,float]:
    return {k: float(v) for k, v in (item.split(":") for item in str_.split(", "))}

def summarize_wins(records:list[Record]) -> str:
    ''' return win - loss - push as percentages of records '''
    wins = len([record for record in records if record.result == 1])
    pushes = len([record for record in records if record.result == 0])
    losses = len([record for record in records if record.result == -1])
    return f"Wins:{wins}, Pushes:{pushes}, Losses:{losses}" # NOTE: may want to format ast or json. ok for now.

def summarize_profit(records:list[Record]) -> str:
    buyin = sum([record.bet_units for record in records]) 
    payout = sum([record.final_payout for record in records])
    return f"Buyin:{buyin}, Payout:{payout}, Net:{round(payout-buyin,1)}" # NOTE: may want to format ast or json. ok for now.

def summarize_ev(records:list[Record]) -> str:
    # NOTE: not 100% sure about this calculation...
    wins_dict = summarize_str_to_dict(summarize_wins(records))
    profit_dict = summarize_str_to_dict(summarize_profit(records))
    observations = sum(list(wins_dict.values()))
    ev = round(profit_dict['Net'] / observations, 4) if observations > 0 else 0
    return f"Net_Units:{profit_dict['Net']}, Obs:{observations}, EV:{ev}"

class Simulator:
    def __init__(
            self,
            chart:Chart, # TODO: add flexible charts in future
            dealer_hit_soft_17:bool = True,
            n_decks: int = 6,
            max_splits:int = 4,
            blackjack_payout:float = 3/2,
            surrender_payout:float = 1/2,
            counter:Counter|None = None
        ):
        self.chart = chart
        self.dealer_hit_soft_17 = dealer_hit_soft_17
        self.n_decks = n_decks
        self.max_splits = max_splits
        self.blackjack_payout = blackjack_payout
        self.surrender_payout = surrender_payout
        self.counter = Counter.from_low_high_cutoffs(6,10) if counter is None else counter
        self._records:list[Record] = []

    @property
    def lookup_keys(self):
        # NOTE: may have to change if/when incorporate flexible charts
        return list(product(self.chart.df.index.to_list(), self.chart.df.columns.to_list()))
    
    @staticmethod
    def _metric_dict_to_df(metric_dict:dict) -> pd.DataFrame:
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
    
    def _filter_records_by_lookup(self, lookup:tuple[int,str]) -> list[Record]:
        return [r for r in self._records if r.chart_lookup == lookup]
    
    def records_to_df(self):
        if len(self._records) == 0:
            print('No records found. Run simulation.')
        else:
            return pd.DataFrame([r.to_dict() for r in self._records])
    
    def output_chart(self, typ:str) -> pd.DataFrame:

        if typ not in ['profit', 'win', 'ev']: # NOTE: should make enums for this but too lazy rn...
            raise ValueError(f"output_chart typ must be in ['profit', 'win', 'ev']. got {typ}")
        
        metric_dict = {}
        for lookup in self.lookup_keys:
            records = self._filter_records_by_lookup(lookup)
            if typ == 'profit':
                output_str = summarize_profit(records)
            if typ == 'win':
                output_str = summarize_wins(records)
            if typ == 'ev':
                output_str = summarize_ev(records)

            metric_dict[lookup] = output_str
            
        return self._metric_dict_to_df(metric_dict)
        
    def output_summary(self):
        return (
            summarize_wins(self._records),
            summarize_profit(self._records),
            summarize_ev(self._records)
        )
    
    def run(self, hands = 10, overwrite:bool=False) -> None:
        
        # simulation / overwrite stuff
        if len(self._records) > 0 and not overwrite:
            raise ValueError(f'non-emtpy records. must set overwrite to True') # safeguard agaisnt overwriting (temp prob)
        
        self._records = []
                
        # shoe stuff
        deck, stop= shuffle_cut_deck(self.n_decks) # stop indicates the position of the cut card
        shoe_counter = 0

        # create ids of minimum length 6th
        id_digits = len(str(hands)) if len(str(hands)) > 6 else 6
        
        hand_counter = 0
        while hand_counter < hands:
            hand_id = get_hand_id(hand_counter, id_digits) 

            # NOTE: doing pre-hand-count for now, but should update for real-time count after
            pre_hand_count = get_count(deck.drawn_cards, self.counter)

            # shoe stuff
            if shoe_counter > stop:
                deck,stop = shuffle_cut_deck(self.n_decks)
            start_n_cards = len(deck) # lazy way to get how many cards used per round...
            
            player_hand, dealer_hand = deal(deck)

            bet = Bet(player_hand, units=1) # TODO: flexible units involving pressing & deck cound
            bets = run_player_actions(bet , dealer_hand, deck, self.chart)
            run_dealer_actions(dealer_hand, bets, deck)

            for bet in bets:
                payout = calculate_payout(bet, dealer_hand, self.blackjack_payout, self.surrender_payout)

                for history in bet.history:
                    self._records.append(Record(
                        hand_id, 
                        history.player_lookup_value, 
                        history.dealer_upcard_value,
                        pre_hand_count,
                        1, # NOTE: only one chart type allowed for now
                        bet.units, 
                        history.action, 
                        history.hit_card,
                        payout
                    ))

            end_n_cards = len(deck)
            shoe_counter += start_n_cards - end_n_cards

            hand_counter +=1
