from threading import Thread
from core.client import MyClient
from asyncio import (get_event_loop)
from data.bot_secret import my_token

from data.data import client_behavior

clients = []
clients_loop = []
clients_thread = []


async def start(client, token):
    await client.start(token, bot=False)


def run_it_forever(loop):
    loop.run_forever()


def log_user(token, i):

    clients.append(MyClient(client_behavior))
    clients_loop.append(get_event_loop())
    clients_loop[i].create_task(start(clients[i], token))
    clients_thread.append(Thread(target=run_it_forever, args=(clients_loop[i],)))
    clients_thread[i].start()


def main():

    print(
        "\n +--------------------------------------------+"
        "\n |        Sniper Giraffe - Bot Farmer         |"
        "\n |         (c) 2019 Revolver Chicken          |"
        "\n +--------------------------------------------+\n"
    )
    log_user(my_token, 0)


if __name__ == '__main__':
    main()
