from blackjack_simulator.components.chart import Chart
from blackjack_simulator.components.deck import Deck
from blackjack_simulator.components.hand import DealerHand
from blackjack_simulator.components.enums import Action, HandState
from blackjack_simulator.components.bet import Bet

def run_player_actions(
        bets:list[Bet]|Bet, 
        dealer_hand:DealerHand, 
        deck:Deck, 
        chart:Chart, 
        max_splits:int=4,
        surrender_backup:Action=Action.HIT # if surrender action on chart, but non-starting hand
    ) -> list[Bet]:

    if isinstance(bets, Bet):
        bets = [bets] # want a list. if hands split, will add to list

    if len(bets) > 1:
        raise ValueError(f'run_player_actions exects a single bet as input. got {bets}.')

    i = 0 # saftey
    while i<20 and any([b.active for b in bets]): # break if no active hands
        for bet in [b for b in bets if b.active]:

            if len(bet.player_hand) == 1: # if bet from split, will only have one card
                bet.player_hand.add_card(deck.draw())

            if bet.player_hand.blackjack:
                bet.state = HandState.BLACKJACK
                continue

            if dealer_hand.blackjack:
                bet.state = HandState.OOF # oof = dealer blackjack :)
                break

            action = chart.action_lookup(dealer_upcard=dealer_hand.upcard, player_hand=bet.player_hand)

            if action == Action.SURRENDER:
                if len(bet.player_hand) == 2:
                    bet.add_action(Action.SURRENDER, dealer_hand.upcard_value) # action added to bet history
                    bet.state = HandState.SURRENDER
                    continue
                else:
                    action = surrender_backup # 

            if action == Action.DOUBLE:
                if len(bet.player_hand) == 2:
                    bet.add_action(Action.DOUBLE, dealer_hand.upcard_value)
                    bet.state = HandState.DOUBLE
                    bet.units *= 2
                    continue
                else:
                    action = Action.HIT # hit if cant double

            if action == Action.SPLIT:
                if len(bets) <= max_splits:
                    bets.remove(bet)
                    split_bets = bet.split(dealer_hand.upcard_value)
                    bets.insert(0, split_bets[0])
                    bets.insert(1, split_bets[1])
                    break # starts loop at the split bets

                else: # if split no longer available, check the chart but look at hand total
                    action = chart.action_lookup(
                        dealer_upcard=dealer_hand.upcard, 
                        player_hand_value=bet.player_hand.total
                    )

            if action == Action.HIT:
                bet.add_action(Action.HIT, dealer_hand.upcard_value)
                bet.player_hand.add_card(deck.draw())
                if bet.player_hand.bust:
                    bet.state = HandState.BUST
                    continue
                if bet.player_hand.total == 21:
                    bet.state = HandState.STAND
                    continue
                break # if bust or stand move to next bet, otherwise restart loop (lookup action of current bet)

            if action == Action.STAND:
                bet.add_action(Action.STAND, dealer_hand.upcard_value)
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
    while i<10 and dealer_hand.active and not dealer_hand.bust and any([b for b in bets if b.state in [HandState.STAND]]):
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
        return bet.units * 4 if bet.state == HandState.DOUBLE else bet.units * 2
    if bet.player_hand.bust:
        return 0
    if bet.player_hand.total > dealer_hand.total:
        return bet.units * 4 if bet.state == HandState.DOUBLE else bet.units * 2
    if bet.player_hand.total < dealer_hand.total:
        return 0
    if bet.player_hand.total == dealer_hand.total:
        return bet.units
