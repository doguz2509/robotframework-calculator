from unittest import TestCase

from rf_calculator.libs import Percent
from rf_calculator.libs.packet_size import PacketSize as PacketSize, PacketSize

eq = {
    '8k': '1K',
    '1000K': '1M',
    '8g': '1G',
    '8000k': '1M',
}

summ_p = {
    '2K': ('8k', '1K'),
    '2M': ('1000K', '1M'),
    '2G': ('8g', '1G'),
    '2.1M': ('8000k', '1.1M')
}

summ_n = {
    '2.1M': ('800k', '1M')
}

ne = {
    '8k': '1.1K',
    '1002K': '1M',
    '8.1g': '1G',
    '8020k': '1M',
}


class TestBitrate(TestCase):
    def test_bit_value(self):
        b0 = PacketSize(0)
        assert b0 == 0, "Wrong output: {}".format(b0)
        print("Type: {}, Value: {}".format(type(b0).__name__, b0))
        b00 = PacketSize(float(0))
        assert str(b00) == '0.0b', "Wrong output: {}".format(b00)
        print("Type: {}, Value: {}".format(type(b0).__name__, b0))
        b1 = PacketSize('1K')
        assert str(b1) == '1.0K', "Wrong output: {}".format(b1)
        print("Type: {}, Value: {}".format(type(b1).__name__, b1))
        b2 = PacketSize('1M')
        assert str(b2) == '1.0M', "Wrong output: {}".format(b2)
        print("Type: {}, Value: {}".format(type(b2).__name__, b2))
        b3 = PacketSize(number=1, rate='K')
        assert str(b3) == '1.0K', "Wrong output: {}".format(b3)
        print("Type: {}, Value: {}".format(type(b3).__name__, b3))
        b4 = PacketSize('1G')
        assert str(b4) == '1.0G', "Wrong output: {}".format(b4)
        print("Type: {}, Value: {}".format(type(b4).__name__, b4))
        # b4 = PacketSize('1.1G')
        # assert str(b4) == '1.1G', "Wrong output: {}".format(b4)
        # print("Type: {}, Value: {}".format(type(b4), b4))
        b5 = PacketSize('1.1446564G')
        print("Format: {0} vs. {0:.1M}".format(b5))
        # print("Format: {:.2f}".format(b5))

    def test_eq(self):
        for _b1, _b2 in eq.items():
            b1, b2 = PacketSize(_b1), PacketSize(_b2)
            assert b1 == b2, "Wrong output: {} == {}".format(b1, b2)
            print("{} == {}".format(b1, b2))

    def test_ne(self):
        for _b1, _b2 in ne.items():
            b1, b2 = PacketSize(_b1), PacketSize(_b2)
            assert b1 != b2, "Wrong output: {} != {}".format(b1.bit_value, b2.bit_value)
            print("{} != {}".format(b1, b2))

    def test_iadd(self):
        p = PacketSize('1M')
        p_add = PacketSize('1K')
        print(f"{p:.1m}")
        p += p_add
        print(f"{p:.4m}")
        p += '1M'
        print(f"{p:.4m}")

    def test_isub(self):
        p = PacketSize('1M')
        p_sub = PacketSize('1K')
        print(f"{p:.1m}")
        p -= p_sub
        print(f"{p:.4m}")
        p -= '0.1M'
        print(f"{p:.4m}")

    def test_sum_positive(self):
        for _sum, (_b1, _b2) in summ_p.items():
            s, b1, b2 = PacketSize(_sum), PacketSize(_b1), PacketSize(_b2)
            _b = [b1, b2]
            r_s = sum(_b)
            assert r_s == s, "Wrong output: {} + {} == {} (Actual: {})".format(b1, b2, s, r_s)
            print("{} + {} == {}".format(b1, b2, s))

    def test_sum_negative(self):
        for _sum, (_b1, _b2) in summ_n.items():
            s, b1, b2 = PacketSize(_sum), PacketSize(_b1), PacketSize(_b2)
            r_s = sum([b1, b2])
            assert r_s != s, "Wrong output: {} + {} == {} (Actual: {})".format(b1, b2, s, r_s)
            print("{} + {} != {} (Actual: {})".format(b1, b2, s, r_s))

    def test_percent(self):
        packet = PacketSize('1M')
        percent = Percent('10%')
        packet += percent
        print(f"{packet}")

    def test_format_conversion(self):
        v = 8000000.8
        p = PacketSize(number=v)
        print(f"{p}")
        print(f"{p:.1b}")
        print(f"{p:.1k}")
        print(f"{p:.2m}")
        print(f"{p:.1B}")
        print(f"{p:.1K}")
        print(f"{p:.1M}")

