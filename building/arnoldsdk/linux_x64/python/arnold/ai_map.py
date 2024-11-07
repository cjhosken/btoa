# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_node_entry import *
from .ai_types import *

class AtParamValueMap(Structure):
    pass

class AtParamValueMapIterator(Structure):
    pass

class AtParamValueMapEntry(Structure):
    _fields_ = [("name", AtStringStruct),
                ("type", c_ubyte),
                ("value", AtParamValue)]

def AiParamValueMap():
    func = ai.AiParamValueMap
    func.argtypes = []
    func.restype = c_void_p
    return NullToNone(func(), POINTER(AtParamValueMap))

AiParamValueMapDestroy = ai.AiParamValueMapDestroy
AiParamValueMapDestroy.argtypes = [POINTER(AtParamValueMap)]
AiParamValueMapDestroy.restype = None

AiParamValueMapMerge = ai.AiParamValueMapMerge
AiParamValueMapMerge.argtypes = [POINTER(AtParamValueMap), POINTER(AtParamValueMap)]
AiParamValueMapMerge.restype = None

def AiParamValueMapClone(source_map):
    func = ai.AiParamValueMapClone
    func.argtypes = [POINTER(AtParamValueMap)]
    func.restype = c_void_p
    return NullToNone(func(source_map), POINTER(AtParamValueMap))

def AiParamValueMapGetIterator(mds):
    func = ai.AiParamValueMapGetIterator
    func.argtypes = [POINTER(AtParamValueMap)]
    func.restype = c_void_p
    return NullToNone(func(mds), POINTER(AtParamValueMapIterator))

AiParamValueMapSetBool = ai.AiParamValueMapSetBool
AiParamValueMapSetBool.argtypes = [POINTER(AtParamValueMap), AtString, c_bool]
AiParamValueMapSetBool.restype = None

AiParamValueMapSetInt = ai.AiParamValueMapSetInt
AiParamValueMapSetInt.argtypes = [POINTER(AtParamValueMap), AtString, c_int]
AiParamValueMapSetInt.restype = None

AiParamValueMapSetFlt = ai.AiParamValueMapSetFlt
AiParamValueMapSetFlt.argtypes = [POINTER(AtParamValueMap), AtString, c_float]
AiParamValueMapSetFlt.restype = None

AiParamValueMapSetVec = ai.AiParamValueMapSetVec
AiParamValueMapSetVec.argtypes = [POINTER(AtParamValueMap), AtString, AtVector]
AiParamValueMapSetVec.restype = None

AiParamValueMapSetVec2 = ai.AiParamValueMapSetVec2
AiParamValueMapSetVec2.argtypes = [POINTER(AtParamValueMap), AtString, AtVector2]
AiParamValueMapSetVec2.restype = None

AiParamValueMapSetRGB = ai.AiParamValueMapSetRGB
AiParamValueMapSetRGB.argtypes = [POINTER(AtParamValueMap), AtString, AtRGB]
AiParamValueMapSetRGB.restype = None

AiParamValueMapSetStr = ai.AiParamValueMapSetStr
AiParamValueMapSetStr.argtypes = [POINTER(AtParamValueMap), AtString, AtString]
AiParamValueMapSetStr.restype = None

AiParamValueMapSetArray = ai.AiParamValueMapSetArray
AiParamValueMapSetArray.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(AtArray)]
AiParamValueMapSetArray.restype = None

AiParamValueMapSetPtr = ai.AiParamValueMapSetPtr
AiParamValueMapSetPtr.argtypes = [POINTER(AtParamValueMap), AtString, c_void_p]
AiParamValueMapSetPtr.restype = None

AiParamValueMapGetBool = ai.AiParamValueMapGetBool
AiParamValueMapGetBool.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(c_bool)]
AiParamValueMapGetBool.restype = c_bool

AiParamValueMapGetInt = ai.AiParamValueMapGetInt
AiParamValueMapGetInt.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(c_int)]
AiParamValueMapGetInt.restype = c_bool

AiParamValueMapGetFlt = ai.AiParamValueMapGetFlt
AiParamValueMapGetFlt.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(c_float)]
AiParamValueMapGetFlt.restype = c_bool

AiParamValueMapGetVec = ai.AiParamValueMapGetVec
AiParamValueMapGetVec.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(AtVector)]
AiParamValueMapGetVec.restype = c_bool

AiParamValueMapGetVec2 = ai.AiParamValueMapGetVec2
AiParamValueMapGetVec2.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(AtVector2)]
AiParamValueMapGetVec2.restype = c_bool

AiParamValueMapGetRGB = ai.AiParamValueMapGetRGB
AiParamValueMapGetRGB.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(AtRGB)]
AiParamValueMapGetRGB.restype = c_bool

AiParamValueMapGetStr = ai.AiParamValueMapGetStr
AiParamValueMapGetStr.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(AtStringStruct)]
AiParamValueMapGetStr.restype = c_bool

AiParamValueMapGetArray = ai.AiParamValueMapGetArray
AiParamValueMapGetArray.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(AtArray)]
AiParamValueMapGetArray.restype = c_bool

AiParamValueMapGetPtr = ai.AiParamValueMapGetPtr
AiParamValueMapGetPtr.argtypes = [POINTER(AtParamValueMap), AtString, POINTER(c_void_p)]
AiParamValueMapGetPtr.restype = c_bool

AiParamValueMapIteratorDestroy = ai.AiParamValueMapIteratorDestroy
AiParamValueMapIteratorDestroy.argtypes = [POINTER(AtParamValueMapIterator)]
AiParamValueMapIteratorDestroy.restype = None

def AiParamValueMapIteratorGetNext(iter):
    func = ai.AiParamValueMapIteratorGetNext
    func.argtypes = [POINTER(AtParamValueMapIterator)]
    func.restype = c_void_p

    return NullToNone(func(iter), POINTER(AtParamValueMapEntry))

AiParamValueMapIteratorFinished = ai.AiParamValueMapIteratorFinished
AiParamValueMapIteratorFinished.argtypes = [POINTER(AtParamValueMapIterator)]
AiParamValueMapIteratorFinished.restype = c_bool
