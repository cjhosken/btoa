# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *

AtEnum = POINTER(AtPythonString)

AiEnumGetValue = ai.AiEnumGetValue
AiEnumGetValue.argtypes = [AtEnum, AtPythonString]
AiEnumGetValue.restype = c_int

_AiEnumGetString = ai.AiEnumGetString
_AiEnumGetString.argtypes = [AtEnum, c_int]
_AiEnumGetString.restype = AtPythonString

def AiEnumGetString(enum_type, index):
    return AtPythonStringToStr(_AiEnumGetString(enum_type, index))
