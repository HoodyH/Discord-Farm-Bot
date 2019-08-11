from core.utils.log import Log
from asyncio import (sleep)
from random import (randrange, choices)
# 565598652450734130


class AutoFarmer(object):

    def __init__(self, farmer_data):
        self.farmer_data = farmer_data
        self.__stop_action = False
        self.__pause_action = False

    @staticmethod
    def _true_false(true_p):
        population = [True, False]
        weights = [true_p, 1 - true_p]
        choice = choices(population, weights)
        return choice[0]

    def _generate_time_action(self):

        key_counter = 0
        time_actions = []
        total_time = 0
        loop_time = self.farmer_data.get('loop_time', 10)

        action = self.farmer_data.get(key_counter)
        while action is not None:

            message = action.get('message', 'mmh...')
            execution_probability = action.get('execution_probability', 1)
            do_after_time = action.get('do_after_time', 1)

            do_action = self._true_false(execution_probability)

            # do this action based on probability given
            if do_action:
                range_min = do_after_time[0]
                range_max = do_after_time[1]
                t = randrange(range_min, range_max)
                total_time += t
                time_actions.append((message, t))

            key_counter += 1
            action = self.farmer_data.get(key_counter)

        # fill the remaining time
        t = loop_time - total_time
        time_actions.append((None, t))

        return time_actions

    async def start_loop(self, user, channel):

        self.__stop_action = False

        while True:
            if self.__stop_action:
                break

            if not self.__pause_action:

                time_actions = self._generate_time_action()
                typing_time = 0
                for action, time in time_actions:
                    await sleep(time - typing_time)  # time in seconds to send the command
                    if action:
                        typing_time = 1
                        await channel.trigger_typing()
                        await sleep(typing_time)
                        await channel.send(action)
                        Log.print_action_log(
                            user,
                            'sent message: "{}" in location: "{}"'.format(action, user.name)
                        )
                    else:
                        typing_time = 0

    def stop_loop(self):
        self.__stop_action = True

    def pause_loop(self):
        self.__pause_action = True

    def resume_loop(self):
        self.__pause_action = False
