from asyncio import (get_event_loop, set_event_loop, sleep, new_event_loop)
from threading import Thread


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


class ThreadScheduler:

    def __init__(self):
        self.threads = []

    @staticmethod
    def create_loop(action):
        # we need to create a new loop for the thread, and set it as the 'default'
        # loop that will be returned by calls to asyncio.get_event_loop() from this thread.
        loop = new_event_loop()
        set_event_loop(loop)
        loop.run_until_complete(action())
        loop.close()

    async def start_loop(self, action):
        try:
            thread = Thread(target=self.create_loop, args=(action,))
            thread.start()
            thread.join()
            self.threads.append(thread)
            return 1

        except Exception as e:
            print(e)
            pass
