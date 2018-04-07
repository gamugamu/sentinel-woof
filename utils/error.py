# -*- coding: utf-8 -*-
from enum import Enum

class Error_code(Enum):
    NO_OP       = -1
    SUCCESS     = 0
    MALFSCHE    = 50

class Error:
    def __init__(self, code=0, info="success"):
        self.code = code
        self.info = info
