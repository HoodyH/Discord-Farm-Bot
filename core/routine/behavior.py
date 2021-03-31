from core.observer import Subject
from core.modules.scheduler import (ThreadScheduler, Scheduler)
from asyncio import (sleep)
from datetime import datetime


class UserBehavior(object):
    """
    Define the Behavior of the user, when go to sleep, when wakeup, when is busy for work etc
    """
    def __init__(self, client_behavior_data):

        self._on_wakeup = Subject()
        self.scheduler = ThreadScheduler()

        self._online = True
        self._user_status = 'online'

        self.client_behavior_data = client_behavior_data
        self.discord_client = None

    async def action(self):
        data = self.client_behavior_data
        while True:
            print(data)
            self.discord_client.change_presence(status='idle')
            print('yoo')
            await sleep(5)

    async def start_cycle(self, discord_client):
        self.discord_client = discord_client
        await self.discord_client.change_presence(status='idle')
        # await self.scheduler.start_loop(self.action)

    def attach_wakeup(self, observer):
        self._on_wakeup.attach(observer)

    @property
    def is_online(self):
        return self._online

    def go_online(self):
        return

    def go_offline(self):
        return
