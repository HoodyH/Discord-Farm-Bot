from core.utils.log import Log
from asyncio import (sleep)


class AutoFarmer(object):

    def __init__(self):
        self.__stop_action = False

    async def start_loop(self, channel, user, messages_to_send):
        self.__stop_action = False

        message = messages_to_send
        time = 3601

        while True:
            if self.__stop_action:
                break
            await channel.send(message)
            Log.print_action_log(
                user,
                'sent message: "{}" in location: "{}"'.format(message, user.name)
            )
            await sleep(time)  # time in seconds to send the command

    def stop_loop(self):
        self.__stop_action = True
