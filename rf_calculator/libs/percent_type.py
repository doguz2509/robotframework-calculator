import logging
import re

from rf_calculator.abstracts import TypeAbstract

_REGEX = re.compile(r'^([\-+])?([\d.]+)(%)?$')


class Percent (TypeAbstract):
    __doc__ = """Percent class allow define percentage comparing of numbers
       Allowed define as:
        - percentage string (5%, 5.5%, +5%, -5%, 0.3%)
        - absolute number (less then 1 translated to *100)
       Signs (-, +) allow define allowed direction of compare up or down from reference number
       No sign means that both direction (up & down) allowed
       """

    # def __new__(mcs, *args, **kwargs):
    #     super(Percent , mcs).__new__(*args, **kwargs)

    def __init__(cls, value, format_round=2):
        _float_units, cls._direction = cls._parse(value)
        super(Percent, cls).__init__(_float_units)

    @staticmethod
    def _parse(value):
        try:
            m = _REGEX.match(str(value))
            assert m is not None, f"Expression not match pattern - '{value}'"
            _direction = m.groups()[0]
            _float = float(m.groups()[1])
            if _float < 1 and m.groups()[2] is None:
                _float *= 100
            assert 0 <= _float <= 100, f"Percent must de decimal number in range between 0-100 only ({_float})"
            return _float, _direction
        except AssertionError:
            raise ValueError(f"Percent must de decimal number in range between 0-100 only")
        except (ValueError, TypeError):
            raise ValueError(f"Percentage given to define in format [-/+]<float>[%] only ({value})")

    def in_range(self, reference, other_number):
        return self - reference <= other_number <= self + reference

    def __str__(self):
        return "{}{0:.0f}".format(
            self._direction if self._direction is not None else r'+/-',
            self.units)

    def __format__(self, format_spec):
        format_expression = f'{{}}{{:{format_spec}}}'
        return format_expression.format(
            self._direction if self._direction is not None else r'+/-',
            float(self) / 100 if format_spec.endswith('%') else float(self))

    @staticmethod
    def from_units(value):
        return Percent(value)

    def __add__(self, other):
        if self._direction is None or self._direction == '+':
            result = other * (1 + self.units / 100)
        else:
            result = other
        logging.debug(f"Number {other} add ({self}) = {result}")
        return result

    def __sub__(self, other):
        if self._direction is None or self._direction == '-':
            result = other * (1 - self.units / 100)
        else:
            result = other
        logging.debug(f"Number {other} sub ({self}) = {result}")
        return result

