from enum import Enum

class CardSuit(Enum):
    CLUBS = "\u2663"
    DIAMONDS = "\u2666"
    HEARTS = "\u2665"
    SPADES = "\u2660"

class CardValue(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

class Action(Enum):
    DOUBLE = 'D'
    HIT = 'H'
    SPLIT = 'SP'
    STAND = 'S'
    SURRENDER = 'SU'

class HandState(Enum): # NOTE hate this name
    ACTIVE = 'ACTIVE'
    BLACKJACK = 'BLACKJACK'
    BUST = 'BUST'
    DOUBLE = 'DOUBLE' # idk about this tbh...
    OOF = 'OOF'
    STAND = 'STAND'
    SURRENDER = 'SURRENDER'
    