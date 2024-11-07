# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *

#
# How to write the structured stats file
AtStatsMode = c_int
AI_STATS_MODE_OVERWRITE = AtStatsMode(0)
AI_STATS_MODE_APPEND    = AtStatsMode(1)

AiStatsSetFileName = ai.AiStatsSetFileName
AiStatsSetFileName.argtypes = [AtPythonString]
AiStatsSetFileName.restype = None

AiStatsGetFileName = ai.AiStatsGetFileName
AiStatsGetFileName.argtypes = []
AiStatsGetFileName.restype = AtPythonString

AiStatsSetMode = ai.AiStatsSetMode
AiStatsSetMode.argtypes = [AtStatsMode]
AiStatsSetMode.restype = None

AiStatsGetMode = ai.AiStatsGetMode
AiStatsGetMode.argtypes = []
AiStatsGetMode.restype = AtStatsMode

AiProfileSetFileName = ai.AiProfileSetFileName
AiProfileSetFileName.argtypes = [AtPythonString]
AiProfileSetFileName.restype = None

_AiProfileGetFileName = ai.AiProfileGetFileName
_AiProfileGetFileName.argtypes = []
_AiProfileGetFileName.restype = AtStringReturn

def AiProfileGetFileName():
    return AtStringToStr(_AiProfileGetFileName())
