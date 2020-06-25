import operator
from typing import List, AnyStr

from robot.api import logger
from robot.api.deco import library, keyword
from robot.errors import FrameworkError

from . import __version__
from .libs import Percent, PacketSize, RobotTime, get_error_info


@library(scope='SUITE', version=__version__)
class CALC:

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    COMPARE_OPERATIONS = {
        '>': Percent.gt,
        '>=': Percent.ge,
        '<': Percent.lt,
        '<=': Percent.le,
        '==': Percent.eq,
        '!=': Percent.ne
    }

    __doc__ = """Providing KW set for perform numbers operation with percent
    
    """

    @staticmethod
    def get_operator(operation):
        return CALC.COMPARE_OPERATIONS[operation]

    @property
    def description(self) -> AnyStr:
        return "Providing KW set for perform numbers operation with percent"

    def get_keyword_names(self) -> List:
        return [
            self.percent_compare.__name__,
            self.percent_get_low_value.__name__,
            self.percent_get_high_value.__name__,
            self.list_get_summery.__name__,
            self.rf_time.__name__
        ]

    @keyword("PERCENT_COMPARE")
    def percent_compare(self, num1, operation, num2, percent):
        try:
            _operator = self.get_operator(operation)
            _num1 = float(num1)
            _num2 = float(num2)
            _res = _operator(_num1, _num2, percent)
            logger.debug(f"Evaluate: {num1}{operation}{num2} for {percent} = {_res}")
            assert _res, f"Numbers ({num1} & {num2}) differ more then on {percent}"
        except AssertionError as e:
            raise AssertionError(f"{self.__class__.__name__}.PERCENT_COMPARE: Reason: {e}")
        except Exception as e:
            f, li = get_error_info()
            raise FrameworkError(f"{self.__class__.__name__} Unexpected Error: {e} (File: {f}; Line: {li})")

    @keyword("PERCENT_GET_LOW_VALUE")
    def percent_get_low_value(self, number, percent):
        return Percent.sub(number, percent)

    @keyword("PERCENT_GET_HIGH_VALUE")
    def percent_get_high_value(self, number, percent):
        return Percent.add(number, percent)

    @keyword("LIST_GET_SUMMERY")
    def list_get_summery(self, *lists, **kwargs):
        _type = kwargs.get('type', int)
        _result: _type = 0
        try:
            for _list in lists:
                if isinstance(_list, (list, tuple)):
                    _result += sum([_type(_item) for _item in _list])
                else:
                    _number = _type(_list)
                    _result += _number
        except (ValueError, IndexError) as e:
            raise FrameworkError(f"{self.__class__.__name__}.list_get_summery: {e}")
        else:
            return _result

    @keyword("RF_MATH_OPERATION")
    def rf_math_operation(self, time_str1, operation, time_str2):
        """

        :param time_str1:
        :param operation:
        :param time_str2:
        :return:
        """
        try:
            if operation in ['eq', '=', '==']:
                op = operator.eq
                time2 = RobotTime(time_str2)
            elif operation in ['ne', '!=', '<>']:
                op = operator.ne
                time2 = RobotTime(time_str2)
            elif operation in ['add', '+']:
                op = operator.add
                time2 = RobotTime(time_str2)
            elif operation in ['sub', '-']:
                op = operator.sub
                time2 = RobotTime(time_str2)
            elif operation in ['div', '/']:
                op = operator.truediv
                time2 = float(time_str2)
            elif operation in ['mul', '*']:
                op = operator.mul
                time2 = float(time_str2)
            else:
                raise ValueError(f"Operator '{operation}' not valid")

            time1 = RobotTime(time_str1)
            return op(time1, time2)
        except Exception as e:
            raise FrameworkError(e)

