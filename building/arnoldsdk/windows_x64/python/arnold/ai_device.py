# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_array import *
from .ai_render import *

AI_DEVICE_TYPE_CPU = 0   # Render using the CPU
AI_DEVICE_TYPE_GPU = 1   # Render using the GPU

AI_DEVICE_MEMORY_TOTAL = 0
AI_DEVICE_MEMORY_FREE = 1
AI_DEVICE_MEMORY_USED = 2

AiDeviceTypeIsSupported = ai.AiDeviceTypeIsSupported
AiDeviceTypeIsSupported.argtypes = [c_int, POINTER(AtString)]
AiDeviceTypeIsSupported.restype = c_bool

AiDeviceSelect = ai.AiDeviceSelect
AiDeviceSelect.argtypes = [POINTER(AtRenderSession), c_int, POINTER(AtArray)]
AiDeviceSelect.restype = c_int

AiDeviceAutoSelect = ai.AiDeviceAutoSelect
AiDeviceAutoSelect.argtypes = [POINTER(AtRenderSession)]
AiDeviceAutoSelect.restype = c_int

AiDeviceGetSelectedType = ai.AiDeviceGetSelectedType
AiDeviceGetSelectedType.argtypes = [POINTER(AtRenderSession)]
AiDeviceGetSelectedType.restype = c_int

AiDeviceGetSelectedIds = ai.AiDeviceGetSelectedIds
AiDeviceGetSelectedIds.argtypes = [POINTER(AtRenderSession), c_int]
AiDeviceGetSelectedIds.restype = POINTER(AtArray)

AiDeviceGetCount = ai.AiDeviceGetCount
AiDeviceGetCount.argtypes = [c_int]
AiDeviceGetCount.restype = c_int

AiDeviceGetIds = ai.AiDeviceGetIds
AiDeviceGetIds.argtypes = [c_int]
AiDeviceGetIds.restype = POINTER(AtArray)

AiDeviceGetNameFunc = ai.AiDeviceGetName
AiDeviceGetNameFunc.argtypes = [c_int, c_uint]
AiDeviceGetNameFunc.restype = AtStringReturn

def AiDeviceGetName(device_type, device_id):
    return AtStringToStr(AiDeviceGetNameFunc(device_type, device_id))

AiDeviceGetMemoryMB = ai.AiDeviceGetMemoryMB
AiDeviceGetMemoryMB.argtypes = [c_int, c_uint, c_int]
AiDeviceGetMemoryMB.restype = c_uint

AiGPUCacheSetDirectory = ai.AiGPUCacheSetDirectory
AiGPUCacheSetDirectory.argtypes = [AtPythonString]
AiGPUCacheSetDirectory.restype = None

AiGPUCacheGetDirectory = ai.AiGPUCacheGetDirectory
AiGPUCacheGetDirectory.argtypes = []
AiGPUCacheGetDirectory.restype = AtStringReturn


