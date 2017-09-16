import time
import threading
from plan.settings import TICK_RATE


class Ticker(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__callbacks = []
        self.__tick_rate = TICK_RATE
        self.__is_ticking = False
        self.daemon = True

    @property
    def callbacks(self):
        return self.__callbacks

    @property
    def tick_rate(self):
        return self.__tick_rate

    @tick_rate.setter
    def tick_rate(self, value):
        if isinstance(value, int):
            cast = value
        else:
            try:
                cast = float(value)
            except ValueError:
                raise TypeError(
                    '{} of type {} is not a valid argument for tick_rate. Must be convertible to float.'
                    .format(value, type(value))
                )
        self.__tick_rate = cast

    @property
    def is_ticking(self):
        return self.__is_ticking

    def add_callback(self, func):
        if func not in self.__callbacks:
            self.__callbacks.append(func)

    def remove_callback(self, func):
        if func in self.__callbacks:
            self.__callbacks.remove(func)

    def start(self, *args, **kwargs):
        self.__is_ticking = True
        super().start(*args, **kwargs)

    def stop(self):
        self.__is_ticking = False

    def run(self):
        while self.__is_ticking:
            for callback in self.__callbacks:
                callback()
            time.sleep(self.tick_rate)
