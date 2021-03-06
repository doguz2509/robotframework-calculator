# Robotframework Calculator

## Introduction

Extension for Robotframework converting Time, Percent, DataPacket into numeric like objects

Allow following math operations 

## Operating
### Math operation:

- Compare - eq, ne, gt, ge, lt, le (Equality allow deviation in percent)
- Add
- Subscript
- Multiple 
- Divide

#### Data formats: 

- TimeInterval        - 2h 34m, ...
- Percent                  - 234 + 20%
- DataPacket (support iperf)  - 1G, 2g, 45m
- Numeric (integer, float) 

#### Keywords:

**Math**

    LIST_SUM          - Allow sumarise provided list of numbers
    NUMERIC_OPERATION - Allow regular ariphmetic, logical, percent operation on numbers (in, float)
    PACKET_OPERATION  - Allow regular ariphmetic, logical, percent operation on DataPacket 
    TIME_OPERATION    - Allow regular ariphmetic, logical, percent operation on TimeIntervals
    
    Look full help in ROBOT_MATH.html

**Conversion**

    GET_PACKET - Convert packet string (1M) into numeric object
    GET_TIME_INTERVAL - Convert time string (1h) into numeric object

### API:

**Data Packet**


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
    
**Time Interval**


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

    
**Percent**


    from robot_math import Percent
    
    p = Percent('10.5%')
    print(f"{p}")
    > 10.50%
    print(f"{p:.1%}")
    > 10.5%
    print(f"{p:.3f}")
    > 0.105
    
## Installation
    
**PIP**
    
    python -m pip install  robotframework-calculator