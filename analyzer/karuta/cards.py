import re
import random
import pytesseract
from pytesseract import Output
from enum import Enum
from PIL import Image
from typing import List

# Include executable in path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
T_CONFIGS = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz --psm 6'


def filter_text(string):
    out = re.sub(r'[^a-zA-Z0-9 ]', '', string)
    return out.strip()


class CardBorder(Enum):
    NO_FRAME = 'no_frame'
    BIT_FRAME = 'bit_frame'
    GEM_FRAME = 'gem_frame'


class Card:

    def __init__(self, image):
        self._image = image
        self.price: int = 0
        self.border: CardBorder = CardBorder.NO_FRAME
        self.edition: int = 1
        self.character = ''
        self.anime = ''
        self.code = 0

    def __repr__(self):
        return f'(Character-{self.character}, Anime:{self.anime}, Border-{self.border})'

    def _read_text(self, area):
        text_crop = self._image.crop(area).convert('1')
        text = pytesseract.image_to_string(text_crop, lang="eng", config=T_CONFIGS)
        return re.sub(r'[^a-zA-Z0-9 ]', '', text).strip()

    def analyze(self):
        """
        Analyze the image and build data card
        """
        w, h = self._image.size
        side_border_dimension = 45
        top_border_dimension = 50

        # character text
        self.character = self._read_text(
            (side_border_dimension, top_border_dimension, w - side_border_dimension, 110)
        )

        # anime text
        self.anime = self._read_text(
            (top_border_dimension, 300, w - side_border_dimension, h - top_border_dimension)
        )

        print(self)

    def calculate_price(self):
        self.price = 0


class Drop:
    """
    Class that analyzes the card deck
    """

    def __init__(self, file):
        self.file = file
        self.drop_dimension = 3
        self.cards_data: List[Card] = []

        # open the file and check if is a 4 cards drop or there are just 3 cards
        img = Image.open(self.file)
        w, h = img.size
        if w > 900:
            self.drop_dimension = 4

        # cut the image in n images with one card per image only
        divider = int(w / self.drop_dimension)
        for idx in range(self.drop_dimension):
            spacer = divider * idx
            area = (0 + spacer, 0, divider + spacer, h)
            img_crop = img.crop(area)
            card = Card(img_crop)
            card.analyze()
            self.cards_data.append(card)

    def get_reaction(self):
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        if self.drop_dimension == 3:
            emojis.pop()
        return random.choice(emojis)
