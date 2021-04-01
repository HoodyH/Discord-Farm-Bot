from discord import Client as DiscordClient
from core.modules.scheduler import Scheduler
from core.routine.behavior import UserBehavior
from core.routine.action import AutoAction, ActionData
from core.utils.log import Log
from data.config import ALLOWED_IDS, TRAINER_ID, LOG_CHANNEL


class Client(DiscordClient):

    def __init__(self, actions_raw: dict):
        super(Client, self).__init__()

        self.user_id = None

        self.actions_raw = actions_raw
        self.actions = []

        self.scheduler = Scheduler()

        self._report_channel = None

    def _pause_farmers(self):
        for auto_farmer in self.actions:
            auto_farmer.pause_loop()

    def _resume_farmers(self):
        for auto_farmer in self.actions:
            auto_farmer.resume_loop()

    async def on_ready(self):

        self.user_id = self.user.id
        Log.print_on_ready(self.user)

        self._report_channel = self.get_channel(LOG_CHANNEL)

    async def on_message(self, message):

        if message.author.id in ALLOWED_IDS:

            if message.author.id == self.user_id:
                for action_raw in self.actions_raw:

                    action_data = ActionData(action_raw)
                    trigger = action_data.trigger

                    if message.content.startswith(trigger):
                        channels = []
                        for channel_id in action_data.channels:
                            channels.append(self.get_channel(channel_id))

                        for channel in channels:
                            action = AutoAction(self.user, action_data)
                            self.actions.append(action)

                            await self.scheduler.start_loop(
                                await action.start_loop(channel, self._report_channel)
                            )

            reactions = [':one:', 'two', ':three:']

            if message.content.startswith('save channel'):
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

        if after.id == TRAINER_ID:

            if str(before.status) != "offline" and str(after.status) == "offline":
                self._pause_farmers()
                await self._report_channel.send('trainer has gone OFF paused')
            elif str(before.status) != str(after.status):
                self._resume_farmers()
                await self._report_channel.send('trainer has gone ON resumed')
            else:
                return
