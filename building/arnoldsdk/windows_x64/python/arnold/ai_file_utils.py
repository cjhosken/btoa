# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_types import *

# Rendering modes
#
AtFileType = c_int
AI_FILE_TYPE_CUSTOM     = AtFileType(0)
AI_FILE_TYPE_TEXTURE    = AtFileType(1)
AI_FILE_TYPE_OSL        = AtFileType(2)
AI_FILE_TYPE_PROCEDURAL = AtFileType(3)
AI_FILE_TYPE_PLUGIN     = AtFileType(4)

def AiResolveFilePath(file_path, file_type, custom_path = None):
    func = ai.AiResolveFilePath
    func.argtypes = [AtPythonString, AtFileType, AtPythonString]
    func.restype = AtPythonString

    return func(file_path, file_type, custom_path)

