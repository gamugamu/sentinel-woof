# -*- coding: utf-8 -*-
from enum import Enum

class Error_code(Enum):
    NO_OP       = -1
    SUCCESS     = 0
    INVGRANT    = 10
    USERNOTFD   = 20
    MALFSCHE    = 50
    PETNAMEEX   = 110
    PETMAXLIM   = 111

class Error:
    def __init__(self, code=Error_code.SUCCESS, info="success"):
        self.code = code
        self.info = info

    def __str__(self):
        return "error code: %u" % self.code.value

    def to_dict(self):
        return {"code" : self.code.value, "info" : self.info}
