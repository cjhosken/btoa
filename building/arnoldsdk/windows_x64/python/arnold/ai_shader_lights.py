# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_color import *
from .ai_nodes import *
from .ai_vector import *

AiLightIESLoad = ai.AiLightIESLoad
AiLightIESLoad.argtypes = [AtPythonString, c_uint32, c_uint32, POINTER(c_float), POINTER(c_float)]
AiLightIESLoad.restype = c_bool
