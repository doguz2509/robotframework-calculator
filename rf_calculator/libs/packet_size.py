
import enum
import operator
import re

from rf_calculator.abstracts import TypeAbstract
from rf_calculator.libs import Percent


class BitrateFormat(enum.IntEnum):
    b = 1
    B = 8
    k = 1000
    K = 1000 * 8
    m = 1000000
    M = 1000000 * 8
    g = 1000000000
    G = 1000000000 * 8


BITRATE_REGEX = re.compile(r'([\d.]+)(.*)')


class PacketSize(TypeAbstract):
    def __init__(cls, value_str=None, **kwargs):
        value_str = '0' if value_str == 0 else value_str
        rate = kwargs.get('rate', '')
        parsing_value = value_str or f"{kwargs.get('number', '')}{rate}"
        if parsing_value == '':
            raise ValueError(f"Packet size not provided: neither in '{value_str}' or '{kwargs}")
        number, rate_name = cls.parse(parsing_value)
        cls._rate = BitrateFormat[rate_name if rate == '' else rate]
        super().__init__(number * cls._rate)

    @property
    def rate(cls):
        return cls._rate

    def _to_string(cls, format_spec, rate=None):
        rate = BitrateFormat[rate] if rate else cls._rate
        return f"{cls.units / rate:{format_spec}}{rate.name}"

    def __format__(self, format_spec):
        rates = [r for r in list(BitrateFormat) if format_spec.endswith(r.name)]
        if len(rates) == 1:
            rate = rates[0].name
            format_spec = format_spec.replace(rate, 'f')
            return self._to_string(format_spec, rate=rate)
        elif len(rates) == 0:
            return self._to_string(format_spec)
        else:
            raise IndexError()

    def __str__(self):
        return self._to_string('')

    @staticmethod
    def parse(bitrate_str: str):
        try:
            m = BITRATE_REGEX.match(str(bitrate_str))
            if m is None:
                raise AttributeError("Wrong bitrate format ({})".format(bitrate_str))
            number = float(m.groups()[0])
            rate = m.groups()[1] or BitrateFormat.b.name
            return number, rate
        except Exception as e:
            raise type(e)("Cannot parse PacketSize value string '{}' with error: {}".format(bitrate_str, e))

    @staticmethod
    def from_units(value, rate=BitrateFormat.k):
        if isinstance(value, str):
            return PacketSize(value, rate=rate)
        return PacketSize(number=value, rate=rate)

    def _compare_operation(self, other, operation: operator):
        if isinstance(other, str):
            other = PacketSize(other)

        if type(other) == PacketSize:
            return operation(self.units, other.units)
        elif isinstance(other, (int, float)):
            return operation(self.units, other)
        raise ValueError("Argument '{}' not match operation {}".format(other, operation))

    def _execute_operation(self, other, operation: operator):
        if isinstance(other, str):
            other = PacketSize(other)

        if type(other) == Percent:
            result_rate = self.rate
            result_number = operation(other, self.units)
        elif type(other) == PacketSize:
            result_rate = self.rate if self.rate > other.rate else other.rate
            result_number = operation(self.units, other.units) / result_rate
        elif isinstance(other, (int, float)):
            result_rate = self.rate
            result_number = operation(self.units, other) / result_rate
        else:
            raise ValueError("Argument '{}' not match operation {}".format(other, operation))

        return PacketSize(number=result_number, rate=result_rate.name)

    def __eq__(self, other):
        return self._compare_operation(other, operator.eq)

    def __ne__(self, other):
        return self._compare_operation(other, operator.ne)

    def __gt__(self, other):
        return self._compare_operation(other, operator.gt)

    def __ge__(self, other):
        return self._compare_operation(other, operator.ge)

    def __lt__(self, other):
        return self._compare_operation(other, operator.lt)

    def __le__(self, other):
        return self._compare_operation(other, operator.le)

    def __add__(self, other):
        return self._execute_operation(other, operator.add)

    def __iadd__(self, other):
        added = self._execute_operation(other, operator.add)
        self._rate = added._rate
        self._units = added._units
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self + other

    def __sub__(self, other):
        added = self._execute_operation(other, operator.sub)
        self._rate = added._rate
        self._units = added._units
        return self

    def __isub__(self, other):
        subbed = self._execute_operation(other, operator.sub)
        self._rate = subbed._rate
        self._units = subbed._units
        return self

    def __mul__(self, other):
        return self._execute_operation(other, operator.mul)

    def __imul__(self, other):
        return self._execute_operation(other, operator.imul)

    def __truediv__(self, other):
        return self._execute_operation(other, operator.truediv)

    def __itruediv__(self, other):
        return self._execute_operation(other, operator.itruediv)
