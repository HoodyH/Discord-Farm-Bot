import random
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

    def __init__(self, message, file):
        self.drop_dimension = message[34:35]
        self.file = file

        with open("images/file.png", 'wb') as f:
            f.write(self.file.read())

        self.card_data: List[Card] = []

    def get_reaction(self):
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        if self.drop_dimension == 3:
            emojis.pop()
        return random.choice(emojis)
