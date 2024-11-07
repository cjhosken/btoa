# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_types import *
from .ai_map import *
from .ai_nodes import *
from .ai_procedural import *

AtProcViewportMode = c_int
AI_PROC_BOXES = AtProcViewportMode(0)
AI_PROC_POINTS = AtProcViewportMode(1)
AI_PROC_POLYGONS = AtProcViewportMode(2)

AiProceduralViewportFunc = ai.AiProceduralViewport
AiProceduralViewportFunc.argtypes = [POINTER(AtNode), POINTER(AtUniverse), c_int, POINTER(AtParamValueMap)]
AiProceduralViewportFunc.restype = c_int

def AiProceduralViewport(node, universe, mode=AI_PROC_BOXES, params = None):
    return AiProceduralViewportFunc(node, universe, mode, params)

AiProceduralExpandFunc = ai.AiProceduralExpand
AiProceduralExpandFunc.argtypes = [POINTER(AtNode), POINTER(AtParamValueMap)]
AiProceduralExpandFunc.restype = c_bool

def AiProceduralExpand(node, params = None):
    return AiProceduralExpandFunc(node, params)
