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

AiIrradiance = ai.AiIrradiance
AiIrradiance.argtypes = [POINTER(AtVector), POINTER(AtVector), c_ubyte, c_uint32]
AiIrradiance.restype = AtRGB

AiRadiance = ai.AiRadiance
AiRadiance.argtypes = [POINTER(AtVector), POINTER(AtVector), POINTER(AtVector), POINTER(AtNode), c_uint32, c_float, c_float, POINTER(AtNode), c_ubyte, c_uint32]
AiRadiance.restype = AtRGB
