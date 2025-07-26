from __future__ import annotations

from blackjack_simulator.components.enums import Action
from blackjack_simulator.components.card import Card
from blackjack_simulator.components.hand import PlayerHand
from blackjack_simulator.components.chart import Chart


class FlexChart:
    def __init__(self, charts:list[Chart], thresholds:list[int]):
        self._qc_inputs(charts, thresholds)
        self.charts = charts
        self.thresholds = thresholds

    @classmethod
    def from_path(cls, paths:list[str], thresholds:list[int])-> FlexChart:
        ''' from one or more excel/csv '''
        charts = []
        for path in paths:
            if path.endswith('.csv'):
                charts.append(Chart.from_csv(path))
            elif path.endswith('.xlsx'):
                charts.append(Chart.from_excel(path))
            else:
                raise ValueError(f'FlexChart.from_path does not support file type {path.split('.')[-1]}')

        return cls(charts, thresholds)
    
    @classmethod
    def from_sheets(cls, path:str, sheet_names:list[str], thresholds:list[int]) -> FlexChart:
        ''' from sheets from a single excel '''
        charts = []
        for sheet_name in sheet_names:
            charts.append(Chart.from_excel(path, sheet_name=sheet_name))

        return cls(charts, thresholds)

    @staticmethod
    def _qc_inputs(charts:list[Chart], thresholds:list[int]) -> None:
        if not isinstance(charts, list) or not isinstance(thresholds, list):
            raise ValueError(f'charts and thresholds must be lists. got {type(charts)}, {type(thresholds)}')
        
        if not all([isinstance(c,Chart) for c in charts]):
            raise ValueError(f'charts must be list of items type Chart. got {[type(c) for c in charts]}')
        
        if not all([isinstance(i, int) for i in thresholds]):
            raise ValueError(f'thresholds must be list of items type Chart. got {[type(i) for i in thresholds]}')
        
        if not len(charts) > 1:
            raise ValueError(f'FlexChart requires more than 1 chart. use Chart if only one strategy for simulation.')
        
        if not len(charts) == len(thresholds)+1:
            raise ValueError(f'must have one less threshold than chart. got {len(charts)} {len(thresholds)}.')
        
    def _get_chart(self, input_:int) -> Chart:

        if not isinstance(input_, int):
            raise ValueError(f'get_chart requires int. got {type(input_)}')
        
        chart_indx = 0
        for threshold in self.thresholds:
            if input_ < threshold:
                return self.charts[chart_indx]
            else:
                chart_indx += 1
        return self.charts[-1]
    
    def action_lookup(
            self, 
            deck_count:int,
            dealer_upcard_value:int|None=None, 
            dealer_upcard:Card|None=None,
            player_hand:PlayerHand|None=None, 
            player_hand_value:int|None=None
        ) -> Action:

        chart = self._get_chart(deck_count)
        return chart.action_lookup(dealer_upcard_value, dealer_upcard, player_hand, player_hand_value)