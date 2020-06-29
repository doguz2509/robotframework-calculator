# Robotframework Calculator
-----------------
Extension for Robotframework converting Time, Percent, DataPacket into numeric like objects

Allow following math operations 

Math operation:
==============
- Compare - eq, ne, gt, ge, lt, le (Equality allow deviation in percent)
- Add
- Subscript
- Multiple 
- Divide

Data formats: 
====
- Robot time strings        - 2h 34m, ...
- Percents                  - 234 + 20%
- Bitrate (support iperf)  - 1G, 2g, 45m

API:
====
- Data Packet


    from robot_math import DataPacket 
    data_packet1 = DataPacket('1M')

    print(f"{data_paket1}")
    > 1M
    print(f"{data_paket1:K}")
    > 1000000K
    print(f"{data_paket1:b}")
    > 800000000b
    data_paket1 += '0.5M'
    print(f"{data_paket1}")
    > 1.5M
    
- Time Interval


    from robot_math import TimeInterval
    t1 = TimeInterval('1h')
    print(f"{t1}")
    > 1h
    t1 += '20m'
    print(f"{t1}")
    > 1h 20m
    t1 += TimeInterval('20m')
    print(f"{t1}")
    > 1h 40m

- Percent

    
    from robot_math import Percent
    
    p = Percent('10.5%')
    print(f"{p}")
    > 10.50%
    print(f"{p:.1%}")
    > 10.5%
    print(f"{p:.3f}")
    > 0.105