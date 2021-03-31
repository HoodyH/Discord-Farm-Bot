from data.config import TRAINER_ACTIONS, TRAINER_TOKEN
from core.client import Client


def main():
    c = Client(TRAINER_ACTIONS)
    c.run(TRAINER_TOKEN, bot=False)


if __name__ == '__main__':
    main()
