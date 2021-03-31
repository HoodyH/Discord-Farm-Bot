from core.observer import Subject
from core.modules.scheduler import ThreadScheduler, Scheduler
from asyncio import sleep


class UserBehavior(object):
    """
    Define the Behavior of the user, when go to sleep, when wakeup, when is busy for work etc
    """
    def __init__(self):

        self._on_wakeup = Subject()
        self.scheduler = ThreadScheduler()

        self._online = True
        self._user_status = 'online'

        self.discord_client = None

    async def action(self):
        while True:
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
