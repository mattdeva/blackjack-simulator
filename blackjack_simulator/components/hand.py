from blackjack_simulator.components.card import Card
from blackjack_simulator.components.enums import CardValue

class Hand: 
    def __init__(self, cards:list[Card]):
        self.cards = cards
        # self._qc_init()

    def __str__(self):
        return f'Hand({self.cards})'
    
    def __repr__(self):
        return f'Hand({self.cards})'
    
    def __len__(self):
        return len(self.cards)

    @property
    def starting_hand(self) -> bool:
        return True if len(self) == 2 else False
    
    @property
    def blackjack(self) -> bool:
        return True if self.starting_hand and 21 == self.total else False
    
    @property
    def has_ace(self) -> bool:
        return True if CardValue.ACE in [card.value for card in self.cards] else False

    @property
    def soft(self) -> bool:
        return self.has_ace and sum([card.game_value for card in self.cards]) <= 11
    
    @property
    def total(self) -> int:
        # really dont like this
        tmp_sum = sum([card.game_value for card in self.cards])
        
        if self.has_ace and tmp_sum + 10 <= 21:
            if tmp_sum +10 == 21:
                return 21
            else:
                return tmp_sum + 10
        else:
            return tmp_sum
        
    @property
    def bust(self) -> bool:
        return True if self.total > 21 else False

    # seems silly.. but idk appending to the attritbute directly would feel weird
    def add_card(self, card:Card) -> None:
        if not isinstance(card, Card):
            raise ValueError(f'hand.add_card can only accept type Card as input. got {type(card)}')
        self.cards.append(card)


class DealerHand(Hand):
    def __init__(self, cards:list[Card], hit_soft_17:bool = True):
        super().__init__(cards)
        self.hit_soft_17 = hit_soft_17

    def __str__(self):
        return f'DealerHand({self.cards})'
    
    def __repr__(self):
        return f'DealerHand({self.cards})'
    
    @property
    def upcard(self) -> Card:
        return self.cards[1]
    
    @property
    def upcard_value(self) -> CardValue:
        return 'A' if self.upcard.game_value == 1 else self.upcard.game_value # Annoying fix for harcodeding A to 1 earlier
    
    @property # NOTE: not 100% sure about this here while playerhand activity based externally... but i think it makes sense...
    def active(self) -> bool:
        if self.soft and self.hit_soft_17:
            return True if self.total <= 17 else False
        else:
            return True if self.total <17 else False
    

class PlayerHand(Hand):
    def __init__(self, cards:list[Card]):
        super().__init__(cards)

    def __str__(self):
        return f'PlayerHand({self.cards})'
    
    def __repr__(self):
        return f'PlayerHand({self.cards})'
    
    @property
    def splitable(self) -> bool:
        return True if self.starting_hand and self.cards[0].value == self.cards[1].value else False
    
    @property
    def lookup_value(self) -> str|int: # idk about this name...
        if self.splitable and self.has_ace:
            return f"{self.cards[0].value.value},{self.cards[1].value.value}"
        elif self.splitable:
            return f"{self.cards[0].game_value},{self.cards[1].game_value}"
        elif self.soft:
            return f's{self.total}'
        else:
            return self.total