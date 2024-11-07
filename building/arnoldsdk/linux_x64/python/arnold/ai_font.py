# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_array import *  
from .ai_types import *

def AiFontGetFamilies():
    func = ai.AiFontGetFamilies
    func.argtypes = []
    func.restype = POINTER(AtArray)

    return func()

def AiFontGetStyles(family):
    func = ai.AiFontGetStyles
    func.argtypes = [AtString]
    func.restype = POINTER(AtArray)

    return func(family)

def AiFontGetFilename(family, style):
    func = ai.AiFontGetFilename
    func.argtypes = [AtString, AtString]
    func.restype = AtStringReturn

    return AtStringToStr(func(family, style))
