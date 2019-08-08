from discord import Client
from core.modules.scheduler import ThreadScheduler
from core.routine.user_behavior import UserBehavior
from core.routine.auto_farmer import AutoFarmer
from core.utils.log import Log


class MyClient(Client):

    def __init__(self, client_behavior_data):
        super(MyClient, self).__init__()

        self.user_id = None

        self.scheduler = ThreadScheduler()
        self.client_behavior = UserBehavior(client_behavior_data)
        self.auto_farmer = AutoFarmer()

    async def on_ready(self):

        self.user_id = self.user.id
        Log.print_on_ready(self.user)

        await self.client_behavior.start_cycle(self)

    async def on_message(self, message):

        if message.author.id == self.user_id:
            if message.content.startswith('yeet'):
                self.stop_action = False
                await self.scheduler.start_loop(
                    await self.auto_farmer.start_loop(message.channel, self.user, '.timely')
                )

        if message.author.id == self.user_id:
            if message.content.startswith('stop'):
                self.auto_farmer.stop_loop()
                await message.channel.send('ok, stopped')
