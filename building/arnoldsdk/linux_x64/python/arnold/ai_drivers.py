# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

# TODO: Implement all driver functions

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_node_entry import AtNodeEntry
from .ai_types import *

_AiFindDriverType = ai.AiFindDriverType
_AiFindDriverType.argtypes = [AtPythonString]
_AiFindDriverType.restype = c_void_p

def AiFindDriverType(extension):
    return NullToNone(_AiFindDriverType(extension), POINTER(AtNodeEntry))

_AiDriverExtension = ai.AiDriverExtension
_AiDriverExtension.argtypes = [POINTER(AtNodeEntry)]
_AiDriverExtension.restype = c_void_p

def AiDriverExtension(nentry):
    return NullToNone(_AiDriverExtension(nentry), POINTER(AtPythonString))
