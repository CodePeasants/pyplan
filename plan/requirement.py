# Python standard library
import sys

# Package
from plan.serializable import Serializable


class Requirement(Serializable):

    def __init__(self, minimum=None, maximum=None):
        super().__init__()
        self.__min = None
        self.__max = None

        if minimum is not None:
            self.min = minimum
        if maximum is not None:
            self.max = maximum

    def __repr__(self):
        return f'{self.__class__.__name__}({self.min}, {self.max})'

    def __contains__(self, item):
        return self.min <= item <= self.max

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.min == other.min and self.max == other.max
        elif isinstance(other, range):
            return self.min == min(other) and self.max == max(other)
        elif isinstance(other, int):
            return self.min == self.max == other
        else:
            raise TypeError('Invalid type!')

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        return (x for x in range(self.min, self.max+1))

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.min > other.min and self.max > other.max
        elif isinstance(other, range):
            return self.min > min(other) and self.max > max(other)
        elif isinstance(other, int):
            return self.min > other
        else:
            raise TypeError('Invalid type!')

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.min < other.min and self.max < other.max
        elif isinstance(other, range):
            return self.min < min(other) and self.max < max(other)
        elif isinstance(other, int):
            return self.max < other
        else:
            raise TypeError('Invalid type!')

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.min >= other.min and self.max >= other.max
        elif isinstance(other, range):
            return self.min >= min(other) and self.max >= max(other)
        elif isinstance(other, int):
            return self.min >= other
        else:
            raise TypeError('Invalid type!')

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.min <= other.min and self.max <= other.max
        elif isinstance(other, range):
            return self.min <= min(other) and self.max <= max(other)
        elif isinstance(other, int):
            return self.max <= other
        else:
            raise TypeError('Invalid type!')

    @property
    def min(self):
        if self.__min is None:
            return -sys.maxsize
        else:
            return self.__min

    @min.setter
    def min(self, value):
        if self.max is not None and value > self.max:
            raise ValueError(f'Cannot have a min value: {value} greater than max value: {self.max}')
        self.__min = value

    @property
    def max(self):
        if self.__max is None:
            return sys.maxsize
        else:
            return self.__max

    @max.setter
    def max(self, value):
        if self.min is not None and value < self.min:
            raise ValueError(f'Cannot have a max value: {value} less than min value: {self.min}')
        self.__max = value
