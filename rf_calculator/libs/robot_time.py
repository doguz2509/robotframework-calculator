from enum import IntEnum
from robot.utils import timestr_to_secs

__doc__ = """RobotTime are extension for RF robot.utils.timestr_to_secs method
Allow math manipulation with time strings in compatible for RF formats

Examples:
  my_time = RobotTime(1h) + RobotTime(2m)
  print(f"{my_time}")
  > 1h 2m

"""


class RobotTimeUnits(IntEnum):
    s = 1
    m = 60
    h = 60 * 60
    d = 24 * 60 * 60


class RobotTime(type):
    def __new__(mcs, time_interval_str: str = None, **kwargs):
        return super().__new__(mcs, 'RobotTimeInterval', (object,), kwargs)

    def __init__(cls, time_interval):
        super().__init__('RobotTimeInterval')
        cls._seconds = timestr_to_secs(time_interval)

    @staticmethod
    def from_seconds(absolute_seconds):
        return RobotTime(absolute_seconds)

    @staticmethod
    def _seconds_to_timestr(seconds):
        _res_str = ''
        for index, unit in enumerate(reversed(list(RobotTimeUnits))):
            _mod = int(seconds // unit)
            seconds -= _mod * unit
            if _mod > 0:
                _res_str += f'{_mod}{unit.name} '
        return _res_str.strip() if len(_res_str) > 0 else '0'

    def __str__(self):
        return self._seconds_to_timestr(self.seconds)

    @property
    def seconds(cls):
        return cls._seconds

    @staticmethod
    def _normalise(item, accept_number=True):
        if isinstance(item, RobotTime):
            return item.seconds
        else:
            return RobotTime(item).seconds

    def __eq__(self, other):
        return self.seconds == self._normalise(other)

    def __ne__(self, other):
        return not RobotTime.__eq__(self, other)

    def __add__(self, other):
        return self.from_seconds(self.seconds + self._normalise(other))

    def __sub__(self, other):
        return self.from_seconds(self.seconds - self._normalise(other))

    def __idiv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Dividing allowed to numbers only")
        return self.from_seconds(self.seconds / other)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Multiplexing allowed to numbers only")
        return self.from_seconds(self.seconds * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Dividing allowed to numbers only")
        return self.from_seconds(self.seconds / other)

    def __floordiv__(self, other):
        return RobotTime.__truediv__(self, other)

