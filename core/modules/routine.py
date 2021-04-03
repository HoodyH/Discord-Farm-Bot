from abc import ABC, abstractmethod
from asyncio import sleep
from core.modules.scheduler import Scheduler
from datetime import datetime


class Observer(ABC):
    """
    The Observer interface declares the update method, used by DiscordClients.
    """

    @abstractmethod
    async def routine_update(self, is_online: bool) -> None:
        """
        Receive update from the routine manager.
        """
        pass


class _RoutineData:

    def __init__(self, data):
        self.week = []

        schedule = data.get('schedule', {})
        if not schedule:
            print('routine improperly configured, check the schedule')

        # load ordered data into the weeks
        for key in ['mon', 'tue', 'wed', 'thu', 'frd', 'sat', 'sun']:
            self.week.append(schedule.get(key, []))

    def get_today_schedule(self):
        weekday = datetime.now().weekday()
        return self.week[weekday]


class RoutineManager:
    """
    A routine of a singe user
    """

    client = None

    def __init__(self, routine_raw, logger):
        self.routine_data = _RoutineData(routine_raw)
        self.logger = logger

        self.scheduler = Scheduler()

        self.is_online = False

        # follow only trainer routine, and not self generated
        self.follow_trainer_routine = False

    async def _change_presence(self, is_online) -> None:
        """
        Change online status and notify all observers about an event.
        pass the new status
        """
        self.is_online = is_online
        await self.client.routine_update(self.is_online)

    def _generate_time_schedule(self):
        time_schedule = []
        today_schedule = self.routine_data.get_today_schedule()
        now = datetime.now()

        time_converter = 3600  # to seconds

        syncing = True
        last_deactivate = 0

        for idx, schedule in enumerate(today_schedule):
            activate, deactivate = schedule
            last_deactivate = deactivate
            try:
                next_activate, next_deactivate = today_schedule[idx + 1]
            except IndexError:
                next_activate, next_deactivate = None, None

            # on first start do check, sync up with the current time of the day
            # the equal time will be computed inside the active block
            if syncing:
                if activate > now.hour:
                    # is before this block
                    time = (activate - now.hour) * time_converter
                    time_schedule.append((False, time))
                elif activate <= now.hour < deactivate:
                    # is in this block
                    time = (deactivate - now.hour) * time_converter
                    time_schedule.append((True, time))
                elif deactivate < now.hour < next_activate:
                    # between this deactivate and the next activate
                    time = (next_activate - now.hour) * time_converter
                    time_schedule.append((False, time))
                elif deactivate < now.hour >= next_activate:
                    # in a next block
                    continue

                # if this is reached the sync is done
                syncing = False

            else:
                # create time for the future activation block
                active_time = (deactivate - activate) * time_converter
                time_schedule.append((True, active_time))

                # create time for the future idle block
                # if there is a next block fill up to the next start, else fill up to midnight
                if next_activate:
                    inactive_time = (next_activate - deactivate) * time_converter
                    time_schedule.append((False, inactive_time))

        # fill time up with idle up to midnight
        time_schedule.append((False, (24 - last_deactivate) * time_converter))
        return time_schedule

    async def _loop(self) -> None:

        while True:

            time_schedule = self._generate_time_schedule()
            await self.logger.log_action(f'calculated the loop for his routine: "{time_schedule}"')

            if not self.follow_trainer_routine:

                for schedule in time_schedule:
                    is_active, time = schedule
                    await self._change_presence(is_active)

                    status = 'active' if is_active else 'idle'
                    await self.logger.log_action(f'changed presence to: "{status}" for time: "{time}"')
                    await sleep(time)

                    # exit the for before update the status if is needed to follow the trainer
                    if self.follow_trainer_routine:
                        break
            else:
                # waiting loop
                await sleep(1)

    async def _start(self) -> None:
        await self.scheduler.start_loop(
            await self._loop()
        )

    async def subscribe(self, client: Observer):
        self.client = client
        await self._start()
