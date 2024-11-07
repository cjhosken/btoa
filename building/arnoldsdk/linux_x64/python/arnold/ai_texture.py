# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_deprecated import *
from .ai_map import *
from .ai_types import *
from .ai_node_entry import *
from .ai_universe import AtUniverse

class AtImage(Structure):
    _fields_ = [
        ("buffer",c_void_p),
        ("width", c_int),
        ("height", c_int),
        ("full_width", c_int),
        ("full_height", c_int),
        ("x", c_int),
        ("y", c_int),
        ("channels", c_int),
        ("format", c_uint8),
        ("aov_names", POINTER(AtArray)),
    ]

AiTextureGetResolutionFunc = ai.AiTextureGetResolution
AiTextureGetResolutionFunc.argtypes = [AtPythonString, POINTER(c_uint), POINTER(c_uint)]
AiTextureGetResolutionFunc.restype = c_bool

def AiTextureGetResolution(filename):
    width = c_uint(0)
    height = c_uint(0)
    success = AiTextureGetResolutionFunc(filename, width, height)
    return (int(width.value), int(height.value)) if success else None

AiTextureGetNumChannelsFunc = ai.AiTextureGetNumChannels
AiTextureGetNumChannelsFunc.argtypes = [AtPythonString, POINTER(c_uint)]
AiTextureGetNumChannelsFunc.restype = c_bool

def AiTextureGetNumChannels(filename):
    num_channels = c_uint(0)
    success = AiTextureGetNumChannelsFunc(filename, num_channels)
    return int(num_channels.value) if success else None

AiTextureGetChannelNameFunc = ai.AiTextureGetChannelName
AiTextureGetChannelNameFunc.argtypes = [AtPythonString, c_uint]
AiTextureGetChannelNameFunc.restype = AtPythonString

def AiTextureGetChannelName(filename, channel_index):
    return AtStringToStr(AiTextureGetChannelNameFunc(filename, channel_index))

AiTextureGetFormatFunc = ai.AiTextureGetFormat
AiTextureGetFormatFunc.argtypes = [AtPythonString, POINTER(c_uint)]
AiTextureGetFormatFunc.restype = c_bool

def AiTextureGetFormat(filename):
    format = c_uint(0)
    success = AiTextureGetFormatFunc(filename, format)
    return int(format.value) if success else None

AiTextureGetBitDepthFunc = ai.AiTextureGetBitDepth
AiTextureGetBitDepthFunc.argtypes = [AtPythonString, POINTER(c_uint)]
AiTextureGetBitDepthFunc.restype = c_bool

def AiTextureGetBitDepth(filename):
    bit_depth = c_uint(0)
    success = AiTextureGetBitDepthFunc(filename, bit_depth)
    return int(bit_depth.value) if success else None

AiTextureGetMatricesFunc = ai.AiTextureGetMatrices
AiTextureGetMatricesFunc.argtypes = [AtPythonString, POINTER(AtMatrix), POINTER(AtMatrix)]
AiTextureGetMatricesFunc.restype = c_bool

def AiTextureGetMatrices(filename):
    world_to_screen = AtMatrix()
    world_to_camera = AtMatrix()
    success = AiTextureGetMatricesFunc(filename, world_to_screen, world_to_camera)
    return {'world_to_screen': world_to_screen, 'world_to_camera': world_to_camera} if success else None

AiTextureInvalidate = ai.AiTextureInvalidate
AiTextureInvalidate.argtypes = [AtPythonString]
AiTextureInvalidate.restype = None

AiTextureAutoTxFlags = ai.AiTextureAutoTxFlags
AiTextureAutoTxFlags.argtypes = [AtPythonString, AtString, POINTER(AtUniverse)]
AiTextureAutoTxFlags.restype = AtStringReturn

AiTextureGetTxFileName = ai.AiTextureGetTxFileName
AiTextureGetTxFileName.argtypes = [AtPythonString, AtString, AtString, POINTER(AtUniverse)]
AiTextureGetTxFileName.restype = AtStringReturn

AiTextureGetTxSourceFileName = ai.AiTextureGetTxSourceFileName
AiTextureGetTxSourceFileName.argtypes = [AtPythonString]
AiTextureGetTxSourceFileName.restype = AtStringReturn

AiTextureTxFileNeedsUpdate = ai.AiTextureTxFileNeedsUpdate
AiTextureTxFileNeedsUpdate.argtypes = [AtPythonString, AtPythonString, AtPythonString]
AiTextureTxFileNeedsUpdate.restype = c_bool

AtMakeTxStatus = c_int
AiTxPending = 0
AiTxError = 1
AiTxUpdated = 2
AiTxUpdate_unneeded = 3
AiTxAborted = 4

def AiMakeTx(file, flags, universe = None):
    func = ai.AiMakeTx
    func.argtypes = [AtPythonString, AtPythonString, POINTER(AtUniverse)]
    func.restype = None
    func(file, flags, universe)

AiMakeTxWaitJob = ai.AiMakeTxWaitJob
AiMakeTxWaitJob.argtypes = [POINTER(POINTER(AtMakeTxStatus)), POINTER(POINTER(AtPythonString)), POINTER(c_uint)]
AiMakeTxWaitJob.restype = c_uint

AiMakeTxAbort = ai.AiMakeTxAbort
AiMakeTxAbort.argtypes = [POINTER(POINTER(AtMakeTxStatus)), POINTER(POINTER(AtPythonString)), POINTER(c_uint)]
AiMakeTxAbort.restype = None

def AiLoadImage(file, format):
    warnings.warn("Call to function AiLoadImage is deprecated. Use AiReadImage", stacklevel=1, category=DeprecationWarning)
    return AiReadImage(file, format)

AiReadImageFunc = ai.AiReadImage
AiReadImageFunc.argtypes = [AtPythonString, c_uint8, POINTER(AtImage), POINTER(AtParamValueMap)]
AiReadImageFunc.restype = c_bool
def AiReadImage(file, format, params = None):
    image = AtImage()
    if AiReadImageFunc(file, format, image, params):
        return image
    else:
        return None

AiWriteImageFunc = ai.AiWriteImage
AiWriteImageFunc.argtypes = [AtPythonString, POINTER(AtImage), POINTER(AtParamValueMap)]
AiWriteImageFunc.restype = c_bool
def AiWriteImage(file, image, params = None):
    return AiWriteImageFunc(file, image, params)

AiResizeImageFunc = ai.AiResizeImage
AiResizeImageFunc.argtypes = [POINTER(AtImage), POINTER(AtImage), POINTER(AtParamValueMap)]
AiResizeImageFunc.restype = c_bool
def AiResizeImage(file, image, params = None):
    return AiResizeImageFunc(file, image, params)
