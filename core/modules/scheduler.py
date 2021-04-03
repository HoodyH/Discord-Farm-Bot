from asyncio import (
    get_event_loop,
    set_event_loop,
    sleep,
)


class Scheduler:

    def __init__(self):
        self.loops = []

    @staticmethod
    async def sleep():
        while True:
            await sleep(5)

    async def start_loop(self, action):
        try:
            loop = get_event_loop()
            set_event_loop(loop)
            loop.run_until_complete(action())
            self.loops.append(loop)
        except Exception as e:
            print(e)
            pass
