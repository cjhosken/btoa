# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

import inspect
import sys
from ctypes import *
from .arnold_common import ai, NullToNone, AtNode
from .ai_color import *
from .ai_types import *
from .ai_vector import *
from .ai_matrix import *

class AtArray(Structure):
   pass

ai.AiArray.argtypes = [c_uint, c_uint, c_uint]
ai.AiArray.restype  = POINTER(AtArray)

def AiArray(nelems, keys, type, *params):
    return ai.AiArray(nelems, keys, type, *params)

_AiArrayAllocate = ai.AiArrayAllocate
_AiArrayAllocate.argtypes = [c_uint32, c_ubyte, c_ubyte]
_AiArrayAllocate.restype = c_void_p

def AiArrayAllocate(nelements, nkeys, type):
    return NullToNone(_AiArrayAllocate(nelements, nkeys, type), POINTER(AtArray))

AiArrayDestroy = ai.AiArrayDestroy
AiArrayDestroy.argtypes = [POINTER(AtArray)]
AiArrayDestroy.restype = None

_AiArrayConvert = ai.AiArrayConvert
_AiArrayConvert.argtypes = [c_uint32, c_ubyte, c_ubyte, c_void_p]
_AiArrayConvert.restype = c_void_p

def AiArrayConvert(nelements, nkeys, type, data):
    return NullToNone(_AiArrayConvert(nelements, nkeys, type, data), POINTER(AtArray))

AiArrayResize = ai.AiArrayResize
AiArrayResize.argtypes = [POINTER(AtArray), c_uint32, c_ubyte]
AiArrayResize.restype = None

_AiArrayCopy = ai.AiArrayCopy
_AiArrayCopy.argtypes = [POINTER(AtArray)]
_AiArrayCopy.restype = c_void_p

def AiArrayCopy(array):
    return NullToNone(_AiArrayCopy(array), POINTER(AtArray))

AiArraySetKey = ai.AiArraySetKey
AiArraySetKey.argtypes = [POINTER(AtArray), c_ubyte, c_void_p]
AiArraySetKey.restype = c_bool

AiArrayMap = ai.AiArrayMap
AiArrayMap.argtypes = [POINTER(AtArray)]
AiArrayMap.restype = c_void_p

AiArrayMapKey = ai.AiArrayMapKey
AiArrayMapKey.argtypes = [POINTER(AtArray), c_ubyte]
AiArrayMapKey.restype = c_void_p

AiArrayUnmap = ai.AiArrayUnmap
AiArrayUnmap.argtypes = [POINTER(AtArray)]
AiArrayUnmap.restype = None

AiArrayGetNumElements = ai.AiArrayGetNumElements
AiArrayGetNumElements.argtypes = [POINTER(AtArray)]
AiArrayGetNumElements.restype = c_uint32

AiArrayGetNumKeys = ai.AiArrayGetNumKeys
AiArrayGetNumKeys.argtypes = [POINTER(AtArray)]
AiArrayGetNumKeys.restype = c_ubyte

AiArrayGetType = ai.AiArrayGetType
AiArrayGetType.argtypes = [POINTER(AtArray)]
AiArrayGetType.restype = c_ubyte

AiArrayGetDataSize = ai.AiArrayGetDataSize
AiArrayGetDataSize.argtypes = [POINTER(AtArray)]
AiArrayGetDataSize.restype = c_size_t

AiArrayGetKeySize = ai.AiArrayGetKeySize
AiArrayGetKeySize.argtypes = [POINTER(AtArray)]
AiArrayGetKeySize.restype = c_size_t

AiArrayInterpolateVec = ai.AiArrayInterpolateVec
AiArrayInterpolateVec.argtypes = [POINTER(AtArray), c_float, c_uint32]
AiArrayInterpolateVec.restype = AtVector

AiArrayInterpolateFlt = ai.AiArrayInterpolateFlt
AiArrayInterpolateFlt.argtypes = [POINTER(AtArray), c_float, c_uint32]
AiArrayInterpolateFlt.restype = c_float

AiArrayInterpolateRGB = ai.AiArrayInterpolateRGB
AiArrayInterpolateRGB.argtypes = [POINTER(AtArray), c_float, c_uint32]
AiArrayInterpolateRGB.restype = AtRGB

AiArrayInterpolateRGBA = ai.AiArrayInterpolateRGBA
AiArrayInterpolateRGBA.argtypes = [POINTER(AtArray), c_float, c_uint32]
AiArrayInterpolateRGBA.restype = AtRGBA

AiArrayInterpolateMtx = ai.AiArrayInterpolateMtx
AiArrayInterpolateMtx.argtypes = [POINTER(AtArray), c_float, c_uint32]
AiArrayInterpolateMtx.restype = AtMatrix

# AtArray getters
#
AiArrayGetBool = ai.AiArrayGetBool
AiArrayGetBool.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetBool.restype = c_bool

AiArrayGetByte = ai.AiArrayGetByte
AiArrayGetByte.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetByte.restype = c_ubyte

AiArrayGetInt = ai.AiArrayGetInt
AiArrayGetInt.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetInt.restype = c_int

AiArrayGetUInt = ai.AiArrayGetUInt
AiArrayGetUInt.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetUInt.restype = c_uint

AiArrayGetFlt = ai.AiArrayGetFlt
AiArrayGetFlt.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetFlt.restype = c_float

_AiArrayGetVec2 = ai.AiArrayGetVec2
_AiArrayGetVec2.argtypes = [POINTER(AtArray), c_uint32]
if return_small_struct_exception:
    _AiArrayGetVec2.restype = AtVector
    def AiArrayGetVec2(array, index):
       tmp = _AiArrayGetVec2(array, index)
       return AtVector2(tmp.x, tmp.y)
else:
    _AiArrayGetVec2.restype = AtVector2
    def AiArrayGetVec2(array, index):
       return _AiArrayGetVec2(array, index)

AiArrayGetVec = ai.AiArrayGetVec
AiArrayGetVec.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetVec.restype = AtVector

AiArrayGetRGB = ai.AiArrayGetRGB
AiArrayGetRGB.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetRGB.restype = AtRGB

AiArrayGetRGBA = ai.AiArrayGetRGBA
AiArrayGetRGBA.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetRGBA.restype = AtRGBA

_AiArrayGetPtr = ai.AiArrayGetPtr
_AiArrayGetPtr.argtypes = [POINTER(AtArray), c_uint32]
_AiArrayGetPtr.restype = c_void_p

def AiArrayGetPtr(array, index):
   return NullToNone(_AiArrayGetPtr(array, index), POINTER(AtNode))

_AiArrayGetStr = ai.AiArrayGetStr
_AiArrayGetStr.argtypes = [POINTER(AtArray), c_uint32]
_AiArrayGetStr.restype = AtStringReturn

def AiArrayGetStr(array, index):
   return AtStringToStr(_AiArrayGetStr(array, index))

_AiArrayGetArray = ai.AiArrayGetArray
_AiArrayGetArray.argtypes = [POINTER(AtArray), c_uint32]
_AiArrayGetArray.restype = c_void_p
def AiArrayGetArray(array, index):
   return NullToNone(_AiArrayGetArray(array, index), POINTER(AtArray))

AiArrayGetMtx = ai.AiArrayGetMtx
AiArrayGetMtx.argtypes = [POINTER(AtArray), c_uint32]
AiArrayGetMtx.restype = AtMatrix

# AtArray setters
#

AiArraySetBool = ai.AiArraySetBool
AiArraySetBool.argtypes = [POINTER(AtArray), c_uint32, c_bool]
AiArraySetBool.restype = c_bool

AiArraySetByte = ai.AiArraySetByte
AiArraySetByte.argtypes = [POINTER(AtArray), c_uint32, c_ubyte]
AiArraySetByte.restype = c_bool

AiArraySetInt = ai.AiArraySetInt
AiArraySetInt.argtypes = [POINTER(AtArray), c_uint32, c_int]
AiArraySetInt.restype = c_bool

AiArraySetUInt = ai.AiArraySetUInt
AiArraySetUInt.argtypes = [POINTER(AtArray), c_uint32, c_uint]
AiArraySetUInt.restype = c_bool

AiArraySetFlt = ai.AiArraySetFlt
AiArraySetFlt.argtypes = [POINTER(AtArray), c_uint32, c_float]
AiArraySetFlt.restype = c_bool

AiArraySetRGB = ai.AiArraySetRGB
AiArraySetRGB.argtypes = [POINTER(AtArray), c_uint32, AtRGB]
AiArraySetRGB.restype = c_bool

AiArraySetRGBA = ai.AiArraySetRGBA
AiArraySetRGBA.argtypes = [POINTER(AtArray), c_uint32, AtRGBA]
AiArraySetRGBA.restype = c_bool

AiArraySetVec2 = ai.AiArraySetVec2
AiArraySetVec2.argtypes = [POINTER(AtArray), c_uint32, AtVector2]
AiArraySetVec2.restype = c_bool

AiArraySetVec = ai.AiArraySetVec
AiArraySetVec.argtypes = [POINTER(AtArray), c_uint32, AtVector]
AiArraySetVec.restype = c_bool

AiArraySetMtx = ai.AiArraySetMtx
AiArraySetMtx.argtypes = [POINTER(AtArray), c_uint32, AtMatrix]
AiArraySetMtx.restype = c_bool

AiArraySetStr = ai.AiArraySetStr
AiArraySetStr.argtypes = [POINTER(AtArray), c_uint32, AtString]
AiArraySetStr.restype = c_bool

AiArraySetPtr = ai.AiArraySetPtr
AiArraySetPtr.argtypes = [POINTER(AtArray), c_uint32, c_void_p]
AiArraySetPtr.restype = c_bool

AiArraySetArray = ai.AiArraySetArray
AiArraySetArray.argtypes = [POINTER(AtArray), c_uint32, POINTER(AtArray)]
AiArraySetArray.restype = c_bool
