import logging
import re

_REGEX = re.compile(r'^([\-+])?([\d.]+)(%)?$')


class Percent:
    __doc__ = """Percent class allow define percentage comparing of numbers
    Allowed define as:
     - percentage string (5%, 5.5%, +5%, -5%, 0.3%)
     - absolute number (less then 1 translated to *100)
    Signs (-, +) allow define allowed direction of compare up or down from reference number
    No sign means that both direction (up & down) allowed
    """

    def __init__(self, value, round_to=2):
        self._round = round_to
        try:
            m = _REGEX.match(str(value))
            assert m is not None, f"Expression not match pattern - '{value}'"
            self._direction = m.groups()[0]
            self._float = float(m.groups()[1])
            if self._float < 1 and m.groups()[2] is None:
                self._float *= 100
            assert 0 <= self._float <= 100, f"Percent must de decimal number in range between 0-100 only ({self._float})"
        except AssertionError:
            raise TypeError(f"Percent must de decimal number in range between 0-100 only")
        except (ValueError, TypeError):
            raise TypeError(f"Percentage given to define in format [-/+]<float>[%] only ({value})")

    def __str__(self):
        format_pattern = f"{self._direction if self._direction is not None else '+-'}{{:.{self._round}f}}%"
        return format_pattern.format(self._float)

    __repr__ = __str__

    @staticmethod
    def _convert(other):
        try:
            _other = float(other)
            return _other
        except ValueError:
            raise ValueError(f"Cannot handle not number values: {other}")

    def __add__(self, other):
        _other = self._convert(other)
        if self._direction is None or self._direction == '+':
            result = round(_other * (1 + self._float / 100), self._round)
        else:
            result = round(_other, self._round)
        logging.debug(f"Number {other} add ({self}) = {result}")
        return result

    def __sub__(self, other):
        _other = self._convert(other)
        if self._direction is None or self._direction == '-':
            result = round(_other * (1 - self._float / 100), self._round)
        else:
            result = round(_other, self._round)

        logging.debug(f"Number {other} sub ({self}) = {result}")
        return result

    def in_range(self, reference, other_number):
        return self - self._convert(reference) <= other_number <= self + self._convert(reference)

    # Operator support
    @staticmethod
    def eq(reference_num, other_num, percent):
        return Percent(percent).in_range(reference_num, other_num)

    @staticmethod
    def ne(reference_num, other_num, percent):
        return not Percent.eq(reference_num, other_num, percent)

    @staticmethod
    def gt(reference_num, other_num, percent):
        return reference_num > Percent.add(other_num, percent)

    @staticmethod
    def ge(reference_num, other_num, percent):
        return reference_num >= Percent.add(other_num, percent)

    @staticmethod
    def lt(reference_num, other_num, percent):
        return reference_num < Percent.sub(other_num, percent)

    @staticmethod
    def le(reference_num, other_num, percent):
        return reference_num <= Percent.sub(other_num, percent)

    @staticmethod
    def add(number, percent):
        return Percent(percent) + number

    @staticmethod
    def sub(number, percent):
        return Percent(percent) - number
