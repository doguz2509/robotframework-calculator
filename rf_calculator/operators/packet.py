from rf_calculator.libs.packet_size import PacketSize


def packet_sum(*packet_list, **kwargs):
    _list = list(packet_list)
    if _list.__len__() == 0:
        return PacketSize(number=0, **kwargs)
    _res = PacketSize(_list.pop())
    while _list.__len__() > 0:
        _next = _list.pop()
        _next.format = _res.rate
        _res += PacketSize(_next, **kwargs)
    return _res


def packet_min(*packet_list, **kwargs):
    _list = list(packet_list)
    if _list.__len__() == 0:
        return PacketSize(number=0, **kwargs)
    _res = PacketSize(_list.pop(), **kwargs)
    while _list.__len__() > 0:
        _next = _list.pop()
        _next.format = _res.rate
        if _next < _res:
            _res = _next
    return _res


def packet_max(*packet_list, **kwargs):
    _list = list(packet_list)
    if _list.__len__() == 0:
        return PacketSize(number=0, **kwargs)
    _res = PacketSize(_list.pop(), **kwargs)
    while _list.__len__() > 0:
        _next = _list.pop()
        _next.format = _res.format
        if _next > _res:
            _res = _next
    return _res
