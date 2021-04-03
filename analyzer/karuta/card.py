from enum import Enum
from typing import List


class CardBorder(Enum):
    NO_FRAME = 'no_frame'
    BIT_FRAME = 'bit_frame'
    GEM_FRAME = 'gem_frame'


class Card:

    def __init__(self):
        self.price: int = 0
        self.border: CardBorder = CardBorder.NO_FRAME
        self.edition: int = 1
        self.code = 0

    def calculate_price(self):
        self.price = 0


class Drop:

    def __init__(self):
        self.drop_dimension = 3
        self.card_data: List[Card] = []
