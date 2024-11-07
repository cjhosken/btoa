# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_node_entry import *
from .ai_types import *

class AtMetadataStore(Structure):
   pass

AiMetaDataGetBool = ai.AiMetaDataGetBool
AiMetaDataGetBool.argtypes = [POINTER(AtNodeEntry), AtString, AtString, POINTER(c_bool)]
AiMetaDataGetBool.restype = c_bool

AiMetaDataGetInt = ai.AiMetaDataGetInt
AiMetaDataGetInt.argtypes = [POINTER(AtNodeEntry), AtString, AtString, POINTER(c_int)]
AiMetaDataGetInt.restype = c_bool

AiMetaDataGetFlt = ai.AiMetaDataGetFlt
AiMetaDataGetFlt.argtypes = [POINTER(AtNodeEntry), AtString, AtString, POINTER(c_float)]
AiMetaDataGetFlt.restype = c_bool

AiMetaDataGetVec = ai.AiMetaDataGetVec
AiMetaDataGetVec.argtypes = [POINTER(AtNodeEntry), AtString, AtString, POINTER(AtVector)]
AiMetaDataGetVec.restype = c_bool

AiMetaDataGetVec2 = ai.AiMetaDataGetVec2
AiMetaDataGetVec2.argtypes = [POINTER(AtNodeEntry), AtString, AtString, POINTER(AtVector2)]
AiMetaDataGetVec2.restype = c_bool

AiMetaDataGetRGB = ai.AiMetaDataGetRGB
AiMetaDataGetRGB.argtypes = [POINTER(AtNodeEntry), AtString, AtString, POINTER(AtRGB)]
AiMetaDataGetRGB.restype = c_bool

AiMetaDataGetStr = ai.AiMetaDataGetStr
AiMetaDataGetStr.argtypes = [POINTER(AtNodeEntry), AtString, AtString, POINTER(AtStringStruct)]
AiMetaDataGetStr.restype = c_bool

AiMetaDataLoadFile = ai.AiMetaDataLoadFile
AiMetaDataLoadFile.argtypes = [AtPythonString]
AiMetaDataLoadFile.restype = c_bool

_AiMetadataStore = ai.AiMetadataStore
_AiMetadataStore.argtypes = []
_AiMetadataStore.restype = c_void_p

def AiMetadataStore():
   return NullToNone(_AiMetadataStore(), POINTER(AtMetadataStore))

AiMetadataStoreDestroy = ai.AiMetadataStoreDestroy
AiMetadataStoreDestroy.argtypes = [POINTER(AtMetadataStore)]
AiMetadataStoreDestroy.restype = None

AiMetadataStoreLoadFromASS = ai.AiMetadataStoreLoadFromASS
AiMetadataStoreLoadFromASS.argtypes = [POINTER(AtMetadataStore), AtString]
AiMetadataStoreLoadFromASS.restype = c_bool

_AiMetadataStoreGetIterator = ai.AiMetadataStoreGetIterator
_AiMetadataStoreGetIterator.argtypes = [POINTER(AtMetadataStore)]
_AiMetadataStoreGetIterator.restype = c_void_p

def AiMetadataStoreGetIterator(mds):
   return NullToNone(_AiMetadataStoreGetIterator(mds), POINTER(AtMetaDataIterator))

_AiMetadataStoreGetIteratorRecursive = ai.AiMetadataStoreGetIteratorRecursive
_AiMetadataStoreGetIteratorRecursive.argtypes = [POINTER(AtMetadataStore), AtString, c_bool]
_AiMetadataStoreGetIteratorRecursive.restype = c_void_p

def AiMetadataStoreGetIteratorRecursive(mds, param, recursive):
   return NullToNone(_AiMetadataStoreGetIteratorRecursive(mds, param, recursive), POINTER(AtMetaDataIterator))

AiMetadataStoreSetBool = ai.AiMetadataStoreSetBool
AiMetadataStoreSetBool.argtypes = [POINTER(AtMetadataStore), AtString, c_bool]
AiMetadataStoreSetBool.restype = None

AiMetadataStoreSetInt = ai.AiMetadataStoreSetInt
AiMetadataStoreSetInt.argtypes = [POINTER(AtMetadataStore), AtString, c_int]
AiMetadataStoreSetInt.restype = None

AiMetadataStoreSetFlt = ai.AiMetadataStoreSetFlt
AiMetadataStoreSetFlt.argtypes = [POINTER(AtMetadataStore), AtString, c_float]
AiMetadataStoreSetFlt.restype = None

AiMetadataStoreSetVec = ai.AiMetadataStoreSetVec
AiMetadataStoreSetVec.argtypes = [POINTER(AtMetadataStore), AtString, AtVector]
AiMetadataStoreSetVec.restype = None

AiMetadataStoreSetVec2 = ai.AiMetadataStoreSetVec2
AiMetadataStoreSetVec2.argtypes = [POINTER(AtMetadataStore), AtString, AtVector2]
AiMetadataStoreSetVec2.restype = None

AiMetadataStoreSetRGB = ai.AiMetadataStoreSetRGB
AiMetadataStoreSetRGB.argtypes = [POINTER(AtMetadataStore), AtString, AtRGB]
AiMetadataStoreSetRGB.restype = None

AiMetadataStoreSetStr = ai.AiMetadataStoreSetStr
AiMetadataStoreSetStr.argtypes = [POINTER(AtMetadataStore), AtString, AtString]
AiMetadataStoreSetStr.restype = None

AiMetadataStoreGetBool = ai.AiMetadataStoreGetBool
AiMetadataStoreGetBool.argtypes = [POINTER(AtMetadataStore), AtString, POINTER(c_bool)]
AiMetadataStoreGetBool.restype = c_bool

AiMetadataStoreGetInt = ai.AiMetadataStoreGetInt
AiMetadataStoreGetInt.argtypes = [POINTER(AtMetadataStore), AtString, POINTER(c_int)]
AiMetadataStoreGetInt.restype = c_bool

AiMetadataStoreGetFlt = ai.AiMetadataStoreGetFlt
AiMetadataStoreGetFlt.argtypes = [POINTER(AtMetadataStore), AtString, POINTER(c_float)]
AiMetadataStoreGetFlt.restype = c_bool

AiMetadataStoreGetVec = ai.AiMetadataStoreGetVec
AiMetadataStoreGetVec.argtypes = [POINTER(AtMetadataStore), AtString, POINTER(AtVector)]
AiMetadataStoreGetVec.restype = c_bool

AiMetadataStoreGetVec2 = ai.AiMetadataStoreGetVec2
AiMetadataStoreGetVec2.argtypes = [POINTER(AtMetadataStore), AtString, POINTER(AtVector2)]
AiMetadataStoreGetVec2.restype = c_bool

AiMetadataStoreGetRGB = ai.AiMetadataStoreGetRGB
AiMetadataStoreGetRGB.argtypes = [POINTER(AtMetadataStore), AtString, POINTER(AtRGB)]
AiMetadataStoreGetRGB.restype = c_bool

AiMetadataStoreGetStr = ai.AiMetadataStoreGetStr
AiMetadataStoreGetStr.argtypes = [POINTER(AtMetadataStore), AtString, POINTER(AtStringStruct)]
AiMetadataStoreGetStr.restype = c_bool

AiMetadataStoreParamSetBool = ai.AiMetadataStoreParamSetBool
AiMetadataStoreParamSetBool.argtypes = [POINTER(AtMetadataStore), AtString, AtString, c_bool]
AiMetadataStoreParamSetBool.restype = None

AiMetadataStoreParamSetInt = ai.AiMetadataStoreParamSetInt
AiMetadataStoreParamSetInt.argtypes = [POINTER(AtMetadataStore), AtString, AtString, c_int]
AiMetadataStoreParamSetInt.restype = None

AiMetadataStoreParamSetFlt = ai.AiMetadataStoreParamSetFlt
AiMetadataStoreParamSetFlt.argtypes = [POINTER(AtMetadataStore), AtString, AtString, c_float]
AiMetadataStoreParamSetFlt.restype = None

AiMetadataStoreParamSetVec = ai.AiMetadataStoreParamSetVec
AiMetadataStoreParamSetVec.argtypes = [POINTER(AtMetadataStore), AtString, AtString, AtVector]
AiMetadataStoreParamSetVec.restype = None

AiMetadataStoreParamSetVec2 = ai.AiMetadataStoreParamSetVec2
AiMetadataStoreParamSetVec2.argtypes = [POINTER(AtMetadataStore), AtString, AtString, AtVector2]
AiMetadataStoreParamSetVec2.restype = None

AiMetadataStoreParamSetRGB = ai.AiMetadataStoreParamSetRGB
AiMetadataStoreParamSetRGB.argtypes = [POINTER(AtMetadataStore), AtString, AtString, AtRGB]
AiMetadataStoreParamSetRGB.restype = None

AiMetadataStoreParamSetStr = ai.AiMetadataStoreParamSetStr
AiMetadataStoreParamSetStr.argtypes = [POINTER(AtMetadataStore), AtString, AtString, AtString]
AiMetadataStoreParamSetStr.restype = None

AiMetadataStoreParamGetBool = ai.AiMetadataStoreParamGetBool
AiMetadataStoreParamGetBool.argtypes = [POINTER(AtMetadataStore), AtString, AtString, POINTER(c_bool)]
AiMetadataStoreParamGetBool.restype = c_bool

AiMetadataStoreParamGetInt = ai.AiMetadataStoreParamGetInt
AiMetadataStoreParamGetInt.argtypes = [POINTER(AtMetadataStore), AtString, AtString, POINTER(c_int)]
AiMetadataStoreParamGetInt.restype = c_bool

AiMetadataStoreParamGetFlt = ai.AiMetadataStoreParamGetFlt
AiMetadataStoreParamGetFlt.argtypes = [POINTER(AtMetadataStore), AtString, AtString, POINTER(c_float)]
AiMetadataStoreParamGetFlt.restype = c_bool

AiMetadataStoreParamGetVec = ai.AiMetadataStoreParamGetVec
AiMetadataStoreParamGetVec.argtypes = [POINTER(AtMetadataStore), AtString, AtString, POINTER(AtVector)]
AiMetadataStoreParamGetVec.restype = c_bool

AiMetadataStoreParamGetVec2 = ai.AiMetadataStoreParamGetVec2
AiMetadataStoreParamGetVec2.argtypes = [POINTER(AtMetadataStore), AtString, AtString, POINTER(AtVector2)]
AiMetadataStoreParamGetVec2.restype = c_bool

AiMetadataStoreParamGetRGB = ai.AiMetadataStoreParamGetRGB
AiMetadataStoreParamGetRGB.argtypes = [POINTER(AtMetadataStore), AtString, AtString, POINTER(AtRGB)]
AiMetadataStoreParamGetRGB.restype = c_bool

AiMetadataStoreParamGetStr = ai.AiMetadataStoreParamGetStr
AiMetadataStoreParamGetStr.argtypes = [POINTER(AtMetadataStore), AtString, AtString, POINTER(AtStringStruct)]
AiMetadataStoreParamGetStr.restype = c_bool
