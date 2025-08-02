from blackjack_simulator.components.chart import Chart
from blackjack_simulator.components.deck import Deck
from blackjack_simulator.components.hand import DealerHand
from blackjack_simulator.components.enums import Action, HandState
from blackjack_simulator.components.bet import Bet
from blackjack_simulator.simulation.counter import Counter
from blackjack_simulator.simulation.flex_chart import FlexChart


def run_player_actions(
        bets:list[Bet]|Bet, 
        dealer_hand:DealerHand, 
        deck:Deck, 
        chart:Chart, # NOTE: not sure about keeping chart variable with potential of FlexChart..
        counter:Counter,
        max_splits:int=3,
        surrender_backup:Action=Action.HIT # if surrender action on chart, but non-starting hand
    ) -> list[Bet]:

    if isinstance(bets, Bet):
        bets = [bets] # want a list. if hands split, will add to list

    if len(bets) > 1:
        raise ValueError(f'run_player_actions exects a single bet as input. got {bets}.')

    i = 0 # saftey
    while i<30 and any([b.active for b in bets]): # break if no active hands
        for bet in [b for b in bets if b.active]:

            if len(bet.player_hand) == 1: # if bet from split, will only have one card
                bet.player_hand.add_card(deck.draw())

            deck_count = counter.get_count(deck.drawn_cards)

            if bet.player_hand.blackjack:
                if len(bets) ==1: # blackjack for user only available on og hand, not splits
                    bet.add_action(Action.NONE, dealer_hand.upcard_value, deck_count)
                    bet.state = HandState.BLACKJACK
                else:
                    bet.add_action(Action.STAND, dealer_hand.upcard_value, deck_count)
                    bet.state = HandState.STAND
                continue

            if dealer_hand.blackjack:
                bet.add_action(Action.NONE, dealer_hand.upcard_value, deck_count)
                bet.state = HandState.OOF # oof = dealer blackjack :)
                break

            if bet.player_hand.bust:
                bet.state = HandState.BUST
                continue
            if bet.player_hand.total == 21:
                bet.state = HandState.STAND
                continue
            
            if isinstance(chart, Chart):
                action = chart.action_lookup(dealer_upcard=dealer_hand.upcard, player_hand=bet.player_hand)
            elif isinstance(chart, FlexChart):
                action = chart.action_lookup(deck_count, dealer_upcard=dealer_hand.upcard, player_hand=bet.player_hand)
            else:
                raise ValueError(f"chart type must be in ['Chart', 'FlexChart']. got {type(chart)}")
            
            if action == Action.SURRENDER:
                if len(bet.player_hand) == 2:
                    bet.add_action(Action.SURRENDER, dealer_hand.upcard_value, deck_count) # action added to bet history
                    bet.state = HandState.SURRENDER
                    continue
                else:
                    action = surrender_backup # 

            if action == Action.DOUBLE:
                if len(bet.player_hand) == 2:
                    # need the card as a seperate variable to log to action prior to adding to hand
                    draw_card = deck.draw()
                    bet.add_action(Action.DOUBLE, dealer_hand.upcard_value, deck_count, draw_card)
                    bet.player_hand.add_card(draw_card)
                    bet.state = HandState.DOUBLE
                    bet.units *= 2
                    continue
                else:
                    action = Action.HIT # hit if cant double

            if action == Action.SPLIT:
                if len(bets) <= max_splits+1:
                    bets.remove(bet)
                    split_bets = bet.split(dealer_hand.upcard_value, deck_count)
                    bets.insert(0, split_bets[0])
                    bets.insert(1, split_bets[1])
                    break # starts loop at the split bets

                else: # if split no longer available, check the chart but look at hand total

                    # NOTE: sloppy, think of a better way after inital enhancement (repeat pattern from above)
                    if isinstance(chart, Chart):
                        action = chart.action_lookup(dealer_upcard=dealer_hand.upcard, player_hand_value=bet.player_hand.total)
                    elif isinstance(chart, FlexChart):
                        action = chart.action_lookup(deck_count, dealer_upcard=dealer_hand.upcard, player_hand_value=bet.player_hand.total)
                    else:
                        raise ValueError(f"chart type must be in ['Chart', 'FlexChart']. got {type(chart)}")
                    
            if action == Action.HIT:
                # need the card as a seperate variable to log to action prior to adding to hand
                draw_card = deck.draw()
                bet.add_action(Action.HIT, dealer_hand.upcard_value, deck_count, draw_card)
                bet.player_hand.add_card(draw_card)

                break # restart loop (lookup action of current bet)

            if action == Action.STAND:
                bet.add_action(Action.STAND, dealer_hand.upcard_value, deck_count)
                bet.state = HandState.STAND
                continue

        i+=1
        if i==20:
            print(f'oops: {[b.player_hand for b in bets]}, {bets[0].player_hand.lookup_value}, {action}')
    return bets

def run_dealer_actions(dealer_hand:DealerHand, bets:list[Bet], deck:Deck) -> None:
    # need to add check here to ensure all bets not active
    if any([b.active for b in bets]):
        raise ValueError(f'bets still active. {[b.state for b in bets]}')

    i = 0 # saftey
    while i<15 and dealer_hand.active and not dealer_hand.bust and any([b for b in bets if b.state in [HandState.STAND, HandState.DOUBLE]]):
        dealer_hand.add_card(deck.draw())
        i+=1

def calculate_payout(bet:Bet, dealer_hand:DealerHand, blackjack_payout:float, surrender_payout:float) -> float:

    # def better way to do this...
    if bet.state == HandState.BLACKJACK and not dealer_hand.blackjack:
        return bet.units * blackjack_payout + bet.units
    if bet.state == HandState.BLACKJACK and dealer_hand.blackjack:
        return bet.units
    if bet.state == HandState.SURRENDER:
        return bet.units * surrender_payout
    if dealer_hand.bust and not bet.player_hand.bust:
        return bet.units * 2
    if bet.player_hand.bust:
        return 0
    if bet.player_hand.total > dealer_hand.total:
        return bet.units * 2
    if bet.player_hand.total < dealer_hand.total:
        return 0
    if bet.player_hand.total == dealer_hand.total:
        return bet.units
    raise ValueError(f'something wrong with payout: {bet}, {dealer_hand}')