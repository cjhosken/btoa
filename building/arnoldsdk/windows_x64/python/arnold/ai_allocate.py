# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *

AiMalloc = ai.AiMalloc
AiMalloc.argtypes = [c_ulong]
AiMalloc.restype = c_void_p

AiRealloc = ai.AiRealloc
AiRealloc.argtypes = [c_void_p, c_ulong]
AiRealloc.restype = c_void_p

AiFree = ai.AiFree
AiFree.argtypes = [c_void_p]
AiFree.restype = None

AiAddMemUsage = ai.AiAddMemUsage
AiAddMemUsage.argtypes = [c_longlong, AtString]
AiAddMemUsage.restype = None
