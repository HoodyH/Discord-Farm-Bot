from data.configs import configs
from core.client import Client

import io
from analyzer.karuta.cards import Drop


def main():
    c = Client(configs.trainer.actions_raw, configs.trainer.routine_raw)
    c.run(configs.trainer.token, bot=False)


if __name__ == '__main__':
    # main()
    with open('images/cards.png', 'rb') as f:
        d = Drop(f)
