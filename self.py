from data.configs import configs
from core.client import Client

import io
from analyzer.karuta.cards import Drop


def main():
    c = Client(configs.trainer.actions_raw, configs.trainer.routine_raw)
    c.run(configs.trainer.token, bot=False)


def test():
    with open('images/cards4-2.png', 'rb') as f:
        d = Drop(f)
        d.calculate_best()
        print(d)
        print(d.get_reaction())


if __name__ == '__main__':
    main()
    # test()
