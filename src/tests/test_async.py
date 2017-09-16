"""
This doesn't actually test any of our code. Just playing with threading + coroutines.
"""

from functools import partial
import unittest
import time
import asyncio
import threading


class Foo:

    def __init__(self):
        self.__run = None

    @property
    def run(self):
        return self.__run

    @run.setter
    def run(self, value):
        if value == self.__run:
            return

        self.__run = value
        if value:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            loop.run_until_complete(self.tick())
            loop.close()

    def set_run(self, value):
        self.run = value

    async def tick(self):
        ctr = 0
        while self.run:
            ctr += 1
            print("ASYNC {}".format(ctr))
            await asyncio.sleep(0.5)


class TestAsync(unittest.TestCase):

    def test_async(self):
        foo = Foo()
        func = partial(foo.set_run, True)
        thread = threading.Thread(target=func)
        thread.daemon = True

        print('BEFORE')
        thread.start()
        time.sleep(0.5)
        foo.run = True
        print('hi')
        time.sleep(1)
        print('bye')
        foo.run = False
        time.sleep(1.5)
        print('fin')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
