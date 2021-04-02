from data.configs import configs
from core.client import Client


def main():
    c = Client(configs.trainer.actions_raw)
    c.run(configs.trainer.token, bot=False)


if __name__ == '__main__':
    main()
