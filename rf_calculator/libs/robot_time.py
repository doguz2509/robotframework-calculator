from enum import IntEnum
from robot.utils import timestr_to_secs

__doc__ = """RobotTime are extension for RF robot.utils.timestr_to_secs method
Allow math manipulation with time strings in compatible for RF formats

Examples:
  my_time = RobotTime(1h) + RobotTime(2m)
  print(f"{my_time}")
  > 1h 2m

"""

from rf_calculator.libs._special_type_abs import _SpecialType
from rf_calculator.libs.percent_type import Percent


class RobotTimeUnits(IntEnum):
    s = 1
    m = 60
    h = 60 * 60
    d = 24 * 60 * 60


class RobotTime(_SpecialType):

    def __init__(cls, value_str):
        super().__init__(timestr_to_secs(value_str))

    @staticmethod
    def from_units(value_str):
        if type(value_str) == RobotTime:
            return value_str
        return RobotTime(value_str)

    @staticmethod
    def _seconds_to_timestr(seconds, leading_unit=RobotTimeUnits.d):
        _res_str = ''
        for index, unit in enumerate([_u for _u in reversed(list(RobotTimeUnits)) if _u <= leading_unit]):
            _mod = int(seconds // unit)
            seconds -= _mod * unit
            if _mod > 0:
                _res_str += f'{_mod}{unit.name} '
        return _res_str.strip() if len(_res_str) > 0 else '0'

    def __str__(self):
        return self._seconds_to_timestr(int(self))

    def __format__(self, format_spec):
        if format_spec != '':
            return self._seconds_to_timestr(int(self), RobotTimeUnits[format_spec])
        else:
            return str(self)

    def __add__(self, other):
        if type(other) == Percent:
            return self.from_units(other + self)
        return super(RobotTime, self).__add__(other)

    def __iadd__(self, other):
        if type(other) == Percent:
            _temp = self.from_units(other + self)
            self._units = _temp.units
            return self
        return super(RobotTime, self).__iadd__(other)

    def __sub__(self, other):
        if type(other) == Percent:
            return self.from_units(other - self)
        return super(RobotTime, self).__sub__(other)
