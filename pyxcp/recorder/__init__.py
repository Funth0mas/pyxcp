#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""XCP Frame Recording Facility.
"""
from dataclasses import dataclass
from enum import IntEnum

try:
    import numpy as np
    import pandas as pd
except ImportError:
    HAS_PANDAS = False
else:
    HAS_PANDAS = True

import rekorder as rec


@dataclass
class XcpLogFileHeader:
    """ """

    num_containers: int
    record_count: int
    size_uncompressed: int
    size_compressed: int
    compression_ratio: float


class FrameCategory(IntEnum):
    """ """

    META = 0
    CMD = 1
    RES = 2
    ERR = 3
    EV = 4
    SERV = 5
    DAQ = 6
    STIM = 7


COUNTER_MAX = 0xFFFF


class XcpLogFileReader:
    """ """

    def __init__(self, file_name):
        self._reader = rec._PyXcpLogFileReader(file_name)

    def get_header(self):
        return XcpLogFileHeader(*self._reader.get_header_as_tuple())

    def __iter__(self):
        while True:
            frames = self._reader.next_block()
            if frames is None:
                break
            for category, counter, timestamp, _, payload in frames:
                yield (category, counter, timestamp, payload)


class XcpLogFileWriter:
    """ """

    def __init__(self, file_name, p=10, c=1):
        self._writer = rec._PyXcpLogFileWriter(file_name, p, c)

    def add_frame(self, category: FrameCategory, counter: int, timestamp: float, payload: bytes):
        self._writer.add_frame(category, counter % (COUNTER_MAX + 1), timestamp, len(payload), payload)

    def finalize(self):
        self._writer.finalize()
