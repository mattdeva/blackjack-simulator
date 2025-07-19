import pandas as pd

from blackjack_simulator.components.chart import Chart
from blackjack_simulator.simulation.simulator import Simulator

from typing import Any

def uniform_list(l:list[Any]) -> bool:
    ''' return bool if all items in a list are the same '''
    return all(i == l[0] for i in l)

def get_different_actions_lookups(simulators:Simulator) -> list[tuple]:
    different_actions = []
    for lookup_key in simulators[0].lookup_keys:
        player_hand_value, dealer_upcard_value = lookup_key

        actions = [s.chart.action_lookup(player_hand_value=player_hand_value, dealer_upcard_value=dealer_upcard_value) for s in simulators]

        if not uniform_list(actions):
            different_actions.append(lookup_key)

    return different_actions

def compare_simulations(simulations:list[Simulator], typ='all') -> pd.DataFrame:
    ''' create dataframe of different actions comparing multiple simulations'''
    different_action_lookups = get_different_actions_lookups(simulations)
    lookup_summary_dict = {action_lookup:[s.output_summary(action_lookup, typ) for s in simulations] for action_lookup in different_action_lookups}

    out_dict = {}
    out_dict['Summary_Overall'] = [s.output_summary(typ=typ) for s in simulations]

    summary_outputs = []
    for simulation in simulations:
        records = []
        for lookup_key in lookup_summary_dict:
            records.extend(simulation.filter_records_by_lookup(lookup_key))
        summary_outputs.append(simulation.summarize_records(records, typ))
    out_dict['Summary_DiffActions'] = summary_outputs
    
    for action, summary in lookup_summary_dict.items():
        out_dict[f'Player: {action[0]} | Dealer Upcard: {action[1]}'] = summary

    df = pd.DataFrame(out_dict).T

    df.columns = [f'simulation_{i+1}' if s.name is None else s.name for i,s in enumerate(simulations)]

    return df