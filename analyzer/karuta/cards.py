import re
import random
import pytesseract
from PIL import Image, ImageOps, ImageFilter
from typing import List

# Include executable in path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class Card:

    def __init__(self, image, card_id):
        self._image = image
        self.id: int = card_id  # the idx of the card in the deck
        self.price: int = 0
        self.edition: int = 1
        self.print_serial: int = 12000
        self.character = ''
        self.anime = ''

        # once generate the card will have a code
        self.code = 0

    def __repr__(self) -> str:
        return f'(Character-{self.character}, Anime-{self.anime}, ' \
               f'Printed-{self.print_serial}, Edition-{self.edition}, Price-{self.price})'

    def __str__(self):
        return f'CARD:\n' \
               f'Character-{self.character}\n' \
               f'Anime-{self.anime}\n' \
               f'Printed-{self.print_serial}\n' \
               f'Edition-{self.edition}\n' \
               f'Price-{self.price}'

    def _read_text(self, area):
        _image = self._image.crop(area).convert('1')
        text = pytesseract.image_to_string(
            _image,
            lang="eng",
            config='-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz --psm 6'
        )
        return re.sub(r'[^a-zA-Z0-9 ]', '', text).strip()

    def _read_edition(self, area) -> (int, int):
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
        text = pytesseract.image_to_string(
            inverted,
            config='-c tessedit_char_whitelist=0123456789 --psm 13 --oem 1'
        )
        # return print_serial, edition
        print_serial, edition = re.sub(r'[^0-9- ]', '', text).strip().split('-')
        return int(print_serial), int(edition)

    def _print_range_value(self) -> float:
        if 0 < self.print_serial <= 50:
            return 30
        elif 50 < self.print_serial <= 100:
            return 20
        elif 100 < self.print_serial <= 400:
            return 10
        elif 400 < self.print_serial <= 700:
            return 8
        elif 700 < self.print_serial <= 1000:
            return 6
        elif 1000 < self.print_serial <= 2000:
            return 4
        elif 2000 < self.print_serial <= 3000:
            return 3.5
        elif 3000 < self.print_serial <= 5000:
            return 3
        elif 5000 < self.print_serial <= 7000:
            return 2.5
        elif 7000 < self.print_serial <= 10000:
            return 2
        else:
            return 1

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

        try:
            self.print_serial, self.edition = self._read_edition(
                (160 - self.id*3, 370, w - 60 - self.id*3, h - 30)
            )
        except Exception as exc:
            print(exc)

    def calculate_price(self) -> None:
        self.price = self._print_range_value() * self.edition


class Drop:
    """
    Class that analyzes the card deck
    """

    def __init__(self, image):
        self._image = image
        self.drop_dimension = 3
        self.cards_data: List[Card] = []

        self.best_cards_data: List[Card] = []

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
            card = Card(img_crop, card_id=idx)
            card.analyze()
            self.cards_data.append(card)

    def __repr__(self):
        return f'{self.cards_data}'

    def __str__(self):
        out = ''
        for card in self.cards_data:
            out += f'{card}\n\n'
        return out

    def calculate_best(self) -> None:
        _last_best_card_price = 0
        _last_best_card_id = 0
        for card in self.cards_data:
            card.calculate_price()
            if _last_best_card_price < card.price:
                _last_best_card_price = card.price
                _last_best_card_id = card.id

        self.best_cards_data.append(self.cards_data[_last_best_card_id])

    def get_reaction(self) -> str:
        # react with the best card
        self.calculate_best()
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        card = random.choice(self.best_cards_data)
        return emojis[card.id]
