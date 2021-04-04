from datetime import datetime
from discord import TextChannel, User


LOG_ON_DISCORD = False


class Logger:
    """
    Action logger specific for each user
    """
    def __init__(self):
        self.channel = None  # discord channel
        self.user = None  # discord obj that represent the user

    @staticmethod
    def get_ready_log(user):
        return f'\nClient successfully connected as:\n' \
               f'Username: {user.name}\nID: {user.id}\n'

    @staticmethod
    def get_action_log(user, action):
        return f'\nUser {user.name}[{user.id}] at {str(datetime.now()).split(".")[0]}\n' \
               f'He has {action}\n'

    async def log_on_ready(self):
        action_log = Logger.get_ready_log(self.user)
        print(action_log)
        if LOG_ON_DISCORD:
            await self.channel.send(action_log)

    async def log_action(self, action):
        action_log = Logger.get_action_log(self.user, action)
        print(action_log)
        if LOG_ON_DISCORD:
            await self.channel.send(action_log)
