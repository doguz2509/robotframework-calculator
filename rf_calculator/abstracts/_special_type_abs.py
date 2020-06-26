
from abc import ABC, abstractmethod


class _SpecialType(ABC, type):
    def __new__(mcs, *args, **kwargs):
        return super().__new__(mcs, mcs.__name__, (object,), kwargs)

    def __init__(cls, units, _type=float):
        super().__init__(cls.__name__)
        try:
            assert isinstance(units, (int, float))
            cls._units: _type = _type(units)
        except Exception:
            raise ValueError(f"Value must be numeric only vs. {units} - ({type(units).__name__})")

    def __float__(self):
        return float(self._units)

    def __int__(self):
        return int(self._units)

    @property
    def units(self) -> float:
        return float(self)

    def cast_to_units(self, value) -> float:
        if type(self) != type(value):
            return float(self.from_units(value))
        return float(value)

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()

    __repr__ = __str__

    @staticmethod
    @abstractmethod
    def from_units(value, **kwargs):
        raise NotImplementedError()

    def __eq__(self, other):
        return self.units == self.cast_to_units(other)

    def __ne__(self, other):
        return not _SpecialType.__eq__(self, other)

    def __add__(self, other):
        return self.from_units(self.units + self.cast_to_units(other))

    def __iadd__(self, other):
        self._units + self.cast_to_units(other)
        return self

    def __sub__(self, other):
        return self.from_units(self.units - self.cast_to_units(other))

    def __isub__(self, other):
        self._units - self.cast_to_units(other)
        return self

    def __idiv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Dividing allowed to numbers only")
        return self.from_units(self.units / self.cast_to_units(other))

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Multiplexing allowed to numbers only")
        return self.from_units(self.units * self.cast_to_units(other))

    def __truediv__(self, other):
        return _SpecialType.__idiv__(self, other)

    def __floordiv__(self, other):
        return _SpecialType.__idiv__(self, other)
