import re
import random
import pytesseract
from PIL import Image, ImageOps, ImageFilter
from typing import List

# Include executable in path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class Card:

    def __init__(self, image, card_number):
        self._image = image
        self.card_number: int = card_number  # idx card in the deck
        self.price: int = 0
        self.print_serial: int = 1
        self.edition: int = 1
        self.character = ''
        self.anime = ''

        # once generate the card will have a code
        self.code = 0

    def __repr__(self):
        return f'(Character-{self.character}, Anime:{self.anime}, Edition-{self.edition}, Printed-{self.print_serial})'

    def _read_text(self, area):
        _image = self._image.crop(area).convert('1')
        text = pytesseract.image_to_string(
            _image,
            lang="eng",
            config='-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz --psm 6'
        )
        return re.sub(r'[^a-zA-Z0-9 ]', '', text).strip()

    def _read_edition(self, area):
        """
        crop the area
        convert to black and white
        upscale the image and use on in a cluster filter
        invert the chroma, black to white - white to black
        read the text with pytesseract
        cleanup the text and slit on the dash (-)
        """
        _image = self._image.crop(area).convert('L')
        w, h = _image.size
        _image = _image.resize((w*10, h*10), Image.ANTIALIAS).filter(ImageFilter.MinFilter(3))
        inverted = ImageOps.invert(_image)
        inverted.show()
        text = pytesseract.image_to_string(
            inverted,
            config='-c tessedit_char_whitelist=0123456789 --psm 13 --oem 1'
        )
        print(text)
        return re.sub(r'[^0-9- ]', '', text).strip().split('-')

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

        self.print_serial, self.edition = self._read_edition(
            (160 - self.card_number*3, 367, w - 70 - self.card_number*3, h - 32)
        )

        print(self)

    def calculate_price(self):
        self.price = 0


class Drop:
    """
    Class that analyzes the card deck
    """

    def __init__(self, image):
        self._image = image
        self.drop_dimension = 3
        self.cards_data: List[Card] = []

        # open the file and check if is a 4 cards drop or there are just 3 cards
        img = Image.open(self._image)
        w, h = img.size
        if w > 900:
            self.drop_dimension = 4

        # cut the image in n images with one card per image only
        divider = int(w / self.drop_dimension)
        for idx in range(self.drop_dimension):
            spacer = divider * idx
            area = (0 + spacer, 0, divider + spacer, h)
            img_crop = img.crop(area)
            card = Card(img_crop, card_number=idx)
            card.analyze()
            self.cards_data.append(card)

    def get_reaction(self):
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        if self.drop_dimension == 3:
            emojis.pop()
        return random.choice(emojis)
