import os
import sys
from collections import namedtuple

from robot_math.types.percent_type import Percent
from robot_math.types.time_interval_type import TimeInterval, RobotTimeUnits
from robot_math.types.data_packet_type import DataPacket, PacketUnit

ERROR_INFO = namedtuple('ERROR_INFO', ['File', 'Line'])
SUPPORTED_TYPES = [int.__name__, float.__name__, DataPacket.__name__, TimeInterval.__name__]


def type_factory(object_name=int):
    if object_name == DataPacket.__name__:
        return DataPacket
    if object_name == TimeInterval.__name__:
        return TimeInterval
    if object_name == 'int':
        return int
    if object_name == 'float':
        return float
    raise TypeError(f"Object name not valid ({object_name}); Supported types: {', '.join(SUPPORTED_TYPES)}")


def format_factory(string: str, main_type, *extra_types):
    for _type in [main_type] + list(extra_types):
        try:
            return _type(string)
        except ValueError:
            pass

    raise ValueError(f"Cannot cast object for '{string}' on provided types: {[main_type] + list(extra_types)}")


def get_error_info():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return ERROR_INFO(File=file_name, Line=exc_tb.tb_lineno)


__all__ = [
    Percent.__name__,
    TimeInterval.__name__,
    DataPacket.__name__,
    format_factory.__name__,
    get_error_info.__name__
]
