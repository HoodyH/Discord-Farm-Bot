import random
from discord import Client as DiscordClient
from discord import Game, Status
from asyncio import sleep
from core.modules.routine import Observer, RoutineManager
from core.modules.action import get_trigger, get_channels
from core.modules.action import ActionsManager
from core.utils.log import Logger
from data.configs import configs


class Client(DiscordClient, Observer):

    def __init__(self, actions_raw: dict, routine_raw: dict):
        super(Client, self).__init__()

        self.actions = ActionsManager(actions_raw)
        self.routine = RoutineManager(routine_raw)

        self.logger = Logger()

    async def routine_update(self, is_online: bool) -> None:
        if is_online:
            # await self.change_presence(status=Status.do_not_disturb, activity=Game('dunno'))
            self.actions.resume()
        else:
            # await self.change_presence(status=Status.do_not_disturb, afk=True, activity=Game('dunno'))
            self.actions.pause()

    async def on_ready(self):

        self.logger.channel = self.get_channel(configs.log_channel)
        self.logger.user = self.user
        await self.logger.log_on_ready()

        # subscribe yourself to your routine
        await self.routine.subscribe(self)

    async def on_message(self, message):

        if message.author.id in configs.allowed_ids:

            if message.author.id == configs.trainer.id:
                for action_raw in self.actions.actions_raw:

                    if message.content.startswith(get_trigger(action_raw)):
                        for channel_id in get_channels(action_raw):
                            await self.actions.create(
                                self.get_channel(channel_id),
                                action_raw,
                                self.logger
                            )

            if message.author.id == configs.target_id:
                trainer_mention_admin, trainer_mention = f'<@!{configs.trainer.id}>', f'<@{configs.trainer.id}>'
                check_string = ' is dropping'
                if (check_string and (trainer_mention_admin or trainer_mention)) in message.content:
                    emojis = ['1️⃣', '2️⃣', '3️⃣']
                    emote = random.choice(emojis)

                    action_log = f'reacted with "{emote}"'
                    await self.logger.log_action(action_log)

                    await sleep(random.randrange(6, 10))
                    await message.add_reaction(emote)

            if message.content.startswith('save channel'):
                self.logger.channel = message.channel
                await message.channel.send('ok, saved')

            if message.content.startswith('pause!'):
                self.actions.pause()
                await message.channel.send('ok, paused')

            if message.content.startswith('resume!'):
                self.actions.resume()
                await message.channel.send('ok, resumed')

            if message.content.startswith('ignore!'):
                self.routine.follow_trainer_routine = not self.routine.follow_trainer_routine
                if self.routine.follow_trainer_routine:
                    await message.channel.send('farmer now based on trainer')
                else:
                    await message.channel.send('Persistent farmer')

    async def on_member_update(self, before, after):

        if self.routine.follow_trainer_routine:
            return

        # if the trainer user goes off disable all the workers
        if after.id == configs.trainer.id:

            if str(before.status) != "offline" and str(after.status) == "offline":
                self.actions.pause()
                await self.logger.log_action('Trainer has gone OFF paused')
            elif str(before.status) != str(after.status):
                self.actions.resume()
                await self.logger.log_action('Trainer has gone ON resumed')
            else:
                return
