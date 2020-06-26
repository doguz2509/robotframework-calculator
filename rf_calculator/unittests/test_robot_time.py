import logging
from unittest import TestCase
import operator
from rf_calculator.libs import RobotTime
from rf_calculator.libs.percent_type import Percent


class TestRobotTimeInterval(TestCase):
    def test_01(self):
        err = {}
        for pattern in ['3d2h45m20s', 1, 2.1, '1', '2.4', '2s', '2m', '3.5h']:
            try:
                item = RobotTime(pattern)
            except Exception as e:
                err.update({pattern: e})
            else:
                print(f"{pattern}: {item}")

        assert len(err) == 0, "Errors:\n{}".format('\n'.join([f"{k}: {v}" for k, v in err.items()]))

    def test_02(self):
        err = {}
        for num1, num2 in [(RobotTime('1h'), RobotTime('20s')),
                           (RobotTime('1h'), RobotTime('22s')),
                           (RobotTime('1h'), RobotTime('60m')),
                           (RobotTime('1h'), 3),
                           (RobotTime('1h'), RobotTime(3))
                           ]:
            print(f'--{num1}, {num2}-----------------')
            for op in (operator.eq, operator.ne, operator.add, operator.sub):
                try:
                    print(f"\t{op.__name__}({num1}, {num2}) = {op(num1, num2)}")
                except Exception as e:
                    err.update({f"{op.__name__}({num1}, {num2})": e})

            print('----------------------------')
        assert len(err) == 0, "Errors:\n{}".format('\n'.join([f"{k}: {v}" for k, v in err.items()]))

    def test_03(self):
        err = {}
        for num1, num2 in [(RobotTime('1h'), 2),
                           (RobotTime('1h'), 4),
                           (RobotTime('1h'), 2.5),
                           (RobotTime('1h'), 3),
                           ]:
            for op in (operator.mul, operator.truediv):
                try:
                    print(f"\t{op.__name__}({num1}, {num2}) = {op(num1, num2)}")
                except Exception as e:
                    err.update({f"{op.__name__}({num1}, {num2})": e})

            print('----------------------------')
        assert len(err) == 0, "Errors:\n{}".format('\n'.join([f"{k}: {v}" for k, v in err.items()]))

    def test_robottime_persent(self):
        t1 = RobotTime('1d')
        p = Percent('10%')
        logging.info(f"Orig time in d: {t1:d}: {t1 + p:d}")
        logging.info(f"Orig time in h: {t1:h}: {t1 + p:h}")
        logging.info(f"Orig time in m: {t1:m}: {t1 + p:m}")
        logging.info(f"Orig time in s: {t1:s}: {t1 + p:s}")
        t1 += p
        print(f"New time: {t1:h}")
