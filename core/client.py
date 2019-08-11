from discord import Client
from core.modules.scheduler import ThreadScheduler
from core.routine.user_behavior import UserBehavior
from core.routine.auto_farmer import AutoFarmer
from core.utils.log import Log


class MyClient(Client):

    def __init__(self, client_behavior_data, actions_data):
        super(MyClient, self).__init__()

        self.user_id = None

        self.scheduler = ThreadScheduler()
        self.client_behavior = UserBehavior(client_behavior_data)
        self.actions_data = actions_data
        self.auto_farmers = []

    async def on_ready(self):

        self.user_id = self.user.id
        Log.print_on_ready(self.user)

        await self.client_behavior.start_cycle(self)

    async def on_message(self, message):

        if message.author.id == self.user_id:

            for key in self.actions_data.keys():
                if message.content.startswith(key):
                    action_data = self.actions_data.get(key)

                    channels = []
                    for channel_id in action_data.get('channels_id'):
                        channels.append(self.get_channel(channel_id))

                    for channel in channels:
                        auto_farmer = AutoFarmer(action_data)
                        self.auto_farmers.append(auto_farmer)

                        await self.scheduler.start_loop(
                            await auto_farmer.start_loop(
                                self.user,
                                channel
                            )
                        )

        if message.author.id == self.user_id:
            if message.content.startswith('stop!'):
                for auto_farmer in self.auto_farmers:
                    auto_farmer.stop_loop()
                await message.channel.send('ok, stopped')
