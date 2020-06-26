# Operator support
from rf_calculator.libs import Percent


def eq(reference_num, other_num, percent):
    return Percent(percent).in_range(reference_num, other_num)


def ne(reference_num, other_num, percent):
    return not eq(reference_num, other_num, percent)


def gt(reference_num, other_num, percent):
    return reference_num > add(other_num, percent)


def ge(reference_num, other_num, percent):
    return reference_num >= add(other_num, percent)


def lt(reference_num, other_num, percent):
    return reference_num < sub(other_num, percent)


def le(reference_num, other_num, percent):
    return reference_num <= sub(other_num, percent)


def add(number, percent):
    return Percent(percent) + number


def sub(number, percent):
    return Percent(percent) - number
