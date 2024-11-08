# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_array import *
from .ai_bbox import *

# Volume file querying

_AiVolumeFileGetChannels = ai.AiVolumeFileGetChannels
_AiVolumeFileGetChannels.argtypes = [AtPythonString]
_AiVolumeFileGetChannels.restype = c_void_p

def AiVolumeFileGetChannels(filename):
    return NullToNone(_AiVolumeFileGetChannels(filename), POINTER(AtArray))

AiVolumeFileGetBBox = ai.AiVolumeFileGetBBox
AiVolumeFileGetBBox.argtypes = [AtPythonString, POINTER(AtArray)]
AiVolumeFileGetBBox.restype = AtBBox

