from discord import Client
from core.modules.scheduler import ThreadScheduler
from core.routine.user_behavior import UserBehavior
from core.routine.auto_farmer import AutoFarmer
from core.utils.log import Log
from data.bot_secret import b_user_id, trainer_id


class MyClient(Client):

    def __init__(self, client_behavior_data, actions_data):
        super(MyClient, self).__init__()

        self.user_id = None
        self._report_channel = None
        self.ignore_updates = False

        self.scheduler = ThreadScheduler()
        self.client_behavior = UserBehavior(client_behavior_data)
        self.actions_data = actions_data
        self.auto_farmers = []

    def _pause_farmers(self):
        for auto_farmer in self.auto_farmers:
            auto_farmer.pause_loop()

    def _resume_farmers(self):
        for auto_farmer in self.auto_farmers:
            auto_farmer.resume_loop()

    async def on_ready(self):

        self.user_id = self.user.id
        Log.print_on_ready(self.user)

        self._report_channel = self.get_channel(610557045875146775)

        await self.client_behavior.start_cycle(self)

    async def on_message(self, message):

        if message.author.id == (self.user_id or b_user_id):

            if message.author.id == self.user_id:
                for key in self.actions_data.keys():
                    if message.content.startswith(key):
                        action_data = self.actions_data.get(key)

                        channels = []
                        for channel_id in action_data.get('channels_id'):
                            channels.append(self.get_channel(channel_id))

                        for channel in channels:
                            auto_farmer = AutoFarmer(self.user, action_data)
                            self.auto_farmers.append(auto_farmer)

                            await self.scheduler.start_loop(
                                await auto_farmer.start_loop(channel, self._report_channel)
                            )

            if message.content.startswith('save_channel'):
                self._report_channel = message.channel
                await message.channel.send('ok, saved')

            if message.content.startswith('pause!'):
                self._pause_farmers()
                await message.channel.send('ok, paused')

            if message.content.startswith('resume!'):
                self._resume_farmers()
                await message.channel.send('ok, resumed')

            if message.content.startswith('ignore!'):
                if self.ignore_updates:
                    self.ignore_updates = False
                    await message.channel.send('farmer now based on feed')
                else:
                    self.ignore_updates = True
                    await message.channel.send('Persistent farmer')

    async def on_member_update(self, before, after):

        if self.ignore_updates:
            return

        if after.id == trainer_id:

            if str(before.status) != "offline" and str(after.status) == "offline":
                self._pause_farmers()
                await self._report_channel.send('trainer has gone OFF paused')
            elif str(before.status) != str(after.status):
                self._resume_farmers()
                await self._report_channel.send('trainer has gone ON resumed')
            else:
                return


