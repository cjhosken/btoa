# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *

ai.AiGetVersion.argtypes = [AtPythonString, AtPythonString, AtPythonString, AtPythonString]
ai.AiGetVersion.restype = AtPythonString

# NOTE: The following two functions differ from Arnold API. They represent the functionality
#       of AiGetVersion() in a Python friendly way

# Returns version numbers as a 4-element list: [arch, major, minor, fix]
def AiGetVersion():
    arch = create_string_buffer(10)
    major = create_string_buffer(10)
    minor = create_string_buffer(10)
    fix = create_string_buffer(20)
    ai.AiGetVersion(arch, major, minor, fix)
    return [arch.value, major.value, minor.value, fix.value]

def AiGetVersionString():
    arch = AtPythonString()
    major = AtPythonString()
    minor = AtPythonString()
    fix = AtPythonString()
    return AtPythonStringToStr(ai.AiGetVersion(arch, major, minor, fix))

_AiGetVersionInfo = ai.AiGetVersionInfo
_AiGetVersionInfo.argtypes = []
_AiGetVersionInfo.restype = AtPythonString

def AiGetVersionInfo():
    return AtPythonStringToStr(_AiGetVersionInfo())

_AiGetCompileOptions = ai.AiGetCompileOptions
_AiGetCompileOptions.argtypes = []
_AiGetCompileOptions.restype = AtPythonString

def AiGetCompileOptions():
    return AtPythonStringToStr(_AiGetCompileOptions())

AiCheckAPIVersion = ai.AiCheckAPIVersion
AiCheckAPIVersion.argtypes = [AtPythonString, AtPythonString, AtPythonString]
AiCheckAPIVersion.restype = c_bool

AiSetAppString = ai.AiSetAppString
AiSetAppString.argtypes = [AtPythonString]
AiSetAppString.restype = None

_AiGetCopyrightNotices = ai.AiGetCopyrightNotices
_AiGetCopyrightNotices.argtypes = [c_int]
_AiGetCopyrightNotices.restype = AtPythonString

AI_COPYRIGHT_NOTICES_CORE = 0
AI_COPYRIGHT_NOTICES_PLUGINS = 1

def AiGetCopyrightNotices(copyright_notice_type):
    return AtPythonStringToStr(_AiGetCopyrightNotices(copyright_notice_type))
