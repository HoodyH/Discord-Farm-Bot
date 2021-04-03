from abc import ABC, abstractmethod
from asyncio import sleep
from core.modules.scheduler import Scheduler


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
        self.data = data


class RoutineManager:
    """
    A routine of a singe user
    """

    client = None

    def __init__(self, routine_raw):
        self.is_online = False
        self.routine_data = _RoutineData(routine_raw)
        self.scheduler = Scheduler()

        # follow only trainer routine, and not self generated
        self.follow_trainer_routine = False

    async def _change_presence(self) -> None:
        """
        Change online status and notify all observers about an event.
        pass the new status
        """
        self.is_online = not self.is_online
        await self.client.routine_update(self.is_online)

    async def _loop(self) -> None:

        while True:

            if not self.follow_trainer_routine:
                await sleep(10)
                await self._change_presence()
            else:
                await sleep(1)

    async def _start(self) -> None:
        await self.scheduler.start_loop(
            await self._loop()
        )

    async def subscribe(self, client: Observer):
        self.client = client
        await self._start()
