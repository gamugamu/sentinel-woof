# -*- coding: utf-8 -*-
from enum import Enum

class Error_code(Enum):
    NO_OP       = -1
    SUCCESS     = 0
    INVGRANT    = 10
    USERNOTFD   = 20
    PETNOTFD    = 25
    MALFSCHE    = 50
    PETNAMEEX   = 110
    PETMAXLIM   = 111
    NOTIMPL     = 150
    BAETOOLARG  = 180
    OUTOFSCOPE  = 190

info_error = {
    Error_code.NO_OP        : "Nothing Happened",
    Error_code.SUCCESS      : "Operation succeed",
    Error_code.INVGRANT     : "Grant token invalid",
    Error_code.USERNOTFD    : "Utilisateur introuvable",
    Error_code.PETNOTFD     : "Pet introuvable",
    Error_code.MALFSCHE     : "Schema invalide",
    Error_code.PETNAMEEX    : "Nom invalide. (Doublon)",
    Error_code.PETMAXLIM    : "Limite de creation de pets atteint",
    Error_code.NOTIMPL      : "Fonction non implémentée",
    Error_code.BAETOOLARG   : "Badge trop large",
    Error_code.OUTOFSCOPE   : "Out of scope"
}

class ErrorException(Exception):
    '''Raise when a specific subset of values in context of app is wrong'''
    def __init__(self, error):
        self.message    = error.__str__
        self.error      = error

        super(ErrorException, self).__init__(self.message, error)

class Error:
    def __init__(self, code=Error_code.SUCCESS, custom_message=None):
        self.code           = code
        self.custom_message = custom_message

    def to_dict(self):
        message = self.custom_message if self.custom_message is not None else info_error[self.code]
        return {"code" : self.code.value, "message": message}

    def __str__(self):
        return str(self.to_dict())
