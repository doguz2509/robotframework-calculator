import os
import sys
from collections import namedtuple

from .percent_type import Percent
from .robot_time import RobotTime
from .packet_size import PacketSize, BitrateFormat

ERROR_INFO = namedtuple('ERROR_INFO', ['File', 'Line'])


def get_error_info():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return ERROR_INFO(File=file_name, Line=exc_tb.tb_lineno)


def format_factory(string: str):
    if string.endswith('%'):
        return Percent(string)
    if len([0 for i in BitrateFormat if string.endswith(i.name)]) > 0:
        return PacketSize(string)
    return RobotTime(string)


__all__ = [
    Percent.__name__,
    RobotTime.__name__,
    PacketSize.__name__,
    format_factory.__name__,
    get_error_info.__name__
]
