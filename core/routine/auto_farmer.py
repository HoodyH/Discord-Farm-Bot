from core.utils.log import Log
from asyncio import (sleep)
from random import (randrange, choices)


class AutoFarmer(object):

    def __init__(self, user, farmer_data):
        self.user = user
        self.farmer_data = farmer_data
        self.__stop_action = False
        self.__pause_action = False

    @staticmethod
    def _true_false(true_p):
        population = [True, False]
        weights = [true_p, 1 - true_p]
        choice = choices(population, weights)
        return choice[0]

    def _generate_time_action(self, is_first=False):

        time_actions = []
        loop_time = self.farmer_data.get('loop_time', 10)

        key_counter = 0
        total_time = 0
        """
        The 0 key in the farmer_data is consider as init point, 
        the random time generated by the 0 is not counted as total_time (loop time),
        because is a random entry point after the previous cycle.
        
        After that the loop will get and create all the actions after the init point, 
        this actions are part of the total loop time.
        
        The time of this action should not exceed the total loop time.
        If you exceed the loop time the loop will become more longer then expected.
        """
        action_data = self.farmer_data.get(key_counter)
        while action_data is not None:

            message = action_data.get('message', 'mmh...')
            execution_probability = action_data.get('execution_probability', 1)

            # on the first call the loop will kick in fast
            if is_first and (key_counter is 0):
                do_after_time = [2, 8]
            else:
                do_after_time = action_data.get('do_after_time', [2, 10])

            # do this action based on execution_probability given
            do_action = self._true_false(execution_probability)
            if do_action:
                t = randrange(do_after_time[0], do_after_time[1])
                if key_counter is not 0:
                    total_time += t
                time_actions.append((message, t))

            key_counter += 1
            action_data = self.farmer_data.get(key_counter)

        """
        If the actions have not reached the loop time in total_time this section will add the remaining time
        for match the loop time given. If the actions exceed the loop time this value will be 0.
        """
        remaining_time = loop_time - total_time
        if remaining_time > 0:
            time_actions.append((None, remaining_time))

        Log.print_action_log(
            self.user,
            'calculate the loop for this task: "{}"'.format(time_actions)
        )
        return time_actions

    async def start_loop(self, channel, report_channel):

        self.__stop_action = False
        # on the first call the loop will kick in fast
        first_loop = True

        while True:
            if self.__stop_action:
                break

            if not self.__pause_action:

                time_actions = self._generate_time_action(is_first=first_loop)
                await report_channel.send(time_actions)

                typing_time = 0
                for action, time in time_actions:
                    await sleep(time - typing_time)  # time in seconds to send the command

                    if action:
                        typing_time = 1
                        await channel.trigger_typing()
                        await sleep(typing_time)
                        await channel.send(action)
                        Log.print_action_log(
                            self.user,
                            'sent message: "{}" in location: "{}"'.format(action, 'channel')
                        )
                    else:
                        typing_time = 0
                first_loop = False

            else:
                first_loop = True
                await sleep(1)

    def stop_loop(self):
        self.__stop_action = True

    def pause_loop(self):
        self.__pause_action = True

    def resume_loop(self):
        self.__pause_action = False
