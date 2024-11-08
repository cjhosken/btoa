# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone, AtNode
from .ai_color import *
from .ai_matrix import *
from .ai_node_entry import *
from .ai_vector import *
from .ai_types import *
from .ai_universe import AtUniverse
import warnings

class AtUserParamIterator(Structure):
    pass

def AiNode(universe, nentry_name, name = "", parent = None):
    func = ai.AiNode
    func.argtypes = [POINTER(AtUniverse), AtString, AtString, POINTER(AtNode)]
    func.restype = c_void_p

    return NullToNone(func(universe, nentry_name, name, parent), POINTER(AtNode))

def AiNodeLookUpByName(universe, name, parent = None):
    func = ai.AiNodeLookUpByName
    func.argtypes = [POINTER(AtUniverse), AtString, POINTER(AtNode)]
    func.restype = c_void_p

    return NullToNone(func(universe, name, parent), POINTER(AtNode))

AiNodeReset = ai.AiNodeReset
AiNodeReset.argtypes = [POINTER(AtNode)]
AiNodeReset.restype = None

AiNodeResetParameter = ai.AiNodeResetParameter
AiNodeResetParameter.argtypes = [POINTER(AtNode), AtPythonString]
AiNodeResetParameter.restype = None

_AiNodeClone = ai.AiNodeClone
_AiNodeClone.argtypes = [POINTER(AtNode), AtString, POINTER(AtNode)]
_AiNodeClone.restype = c_void_p

def AiNodeClone(node, new_name = "", parent = None):
    return NullToNone(_AiNodeClone(node, new_name, parent), POINTER(AtNode))

AiNodeDestroy = ai.AiNodeDestroy
AiNodeDestroy.argtypes = [POINTER(AtNode)]
AiNodeDestroy.restype = c_bool

AiNodeReplace = ai.AiNodeReplace
AiNodeReplace.argtypes = [POINTER(AtNode), POINTER(AtNode), c_bool]
AiNodeReplace.restype = None

AiNodeIs = ai.AiNodeIs
AiNodeIs.argtypes = [POINTER(AtNode), AtString]
AiNodeIs.restype = c_bool

AiNodeDeclare = ai.AiNodeDeclare
AiNodeDeclare.argtypes = [POINTER(AtNode), AtString, AtPythonString]
AiNodeDeclare.restype = c_bool

AiNodeLink = ai.AiNodeLink
AiNodeLink.argtypes = [POINTER(AtNode), AtPythonString, POINTER(AtNode)]
AiNodeLink.restype = c_bool

AiNodeLinkOutput = ai.AiNodeLinkOutput
AiNodeLinkOutput.argtypes = [POINTER(AtNode), AtPythonString, POINTER(AtNode), AtPythonString]
AiNodeLinkOutput.restype = c_bool

AiNodeUnlink = ai.AiNodeUnlink
AiNodeUnlink.argtypes = [POINTER(AtNode), AtPythonString]
AiNodeUnlink.restype = c_bool

AiNodeIsLinked= ai.AiNodeIsLinked
AiNodeIsLinked.argtypes = [POINTER(AtNode), AtPythonString]
AiNodeIsLinked.restype = c_bool

_AiNodeGetLink = ai.AiNodeGetLink
_AiNodeGetLink.argtypes = [POINTER(AtNode), AtPythonString, POINTER(c_int)]
_AiNodeGetLink.restype = c_void_p

def AiNodeGetLink(node, input, comp = None):
    return NullToNone(_AiNodeGetLink(node, input, comp), POINTER(AtNode))

_AiNodeGetLinkOutput = ai.AiNodeGetLinkOutput
_AiNodeGetLinkOutput.argtypes = [POINTER(AtNode), AtPythonString, POINTER(c_int), POINTER(c_int)]
_AiNodeGetLinkOutput.restype = c_void_p

def AiNodeGetLinkOutput(node, input, output_param, output_comp):
    return NullToNone(_AiNodeGetLinkOutput(node, input, output_param, output_comp), POINTER(AtNode))

_AiNodeGetName = ai.AiNodeGetName
_AiNodeGetName.argtypes = [POINTER(AtNode)]
_AiNodeGetName.restype = AtPythonString

def AiNodeGetName(node):
    return AtPythonStringToStr(_AiNodeGetName(node))

_AiNodeGetNodeEntry = ai.AiNodeGetNodeEntry
_AiNodeGetNodeEntry.argtypes = [POINTER(AtNode)]
_AiNodeGetNodeEntry.restype = c_void_p

def AiNodeGetNodeEntry(node):
    return NullToNone(_AiNodeGetNodeEntry(node), POINTER(AtNodeEntry))

AiNodeGetLocalData = ai.AiNodeGetLocalData
AiNodeGetLocalData.argtypes = [POINTER(AtNode)]
AiNodeGetLocalData.restype = c_void_p

AiNodeSetLocalData = ai.AiNodeSetLocalData
AiNodeSetLocalData.argtypes = [POINTER(AtNode), c_void_p]
AiNodeSetLocalData.restype = None

_AiNodeLookUpUserParameter = ai.AiNodeLookUpUserParameter
_AiNodeLookUpUserParameter.argtypes = [POINTER(AtNode), AtString]
_AiNodeLookUpUserParameter.restype = c_void_p

def AiNodeLookUpUserParameter(node, param):
    return NullToNone(_AiNodeLookUpUserParameter(node, param), POINTER(AtUserParamEntry))

_AiNodeGetUserParamIterator = ai.AiNodeGetUserParamIterator
_AiNodeGetUserParamIterator.argtypes = [POINTER(AtNode)]
_AiNodeGetUserParamIterator.restype = c_void_p

def AiNodeGetUserParamIterator(node):
    return NullToNone(_AiNodeGetUserParamIterator(node), POINTER(AtUserParamIterator))

AiUserParamIteratorDestroy = ai.AiUserParamIteratorDestroy
AiUserParamIteratorDestroy.argtypes = [POINTER(AtUserParamIterator)]
AiUserParamIteratorDestroy.restype = None

_AiUserParamIteratorGetNext = ai.AiUserParamIteratorGetNext
_AiUserParamIteratorGetNext.argtypes = [POINTER(AtUserParamIterator)]
_AiUserParamIteratorGetNext.restype = c_void_p

def AiUserParamIteratorGetNext(iter):
    return NullToNone(_AiUserParamIteratorGetNext(iter), POINTER(AtUserParamEntry))

AiUserParamIteratorFinished = ai.AiUserParamIteratorFinished
AiUserParamIteratorFinished.argtypes = [POINTER(AtUserParamIterator)]
AiUserParamIteratorFinished.restype = c_bool

_AiNodeGetProcessedGeometry = ai.AiNodeGetProcessedGeometry
_AiNodeGetProcessedGeometry.argtypes = [POINTER(AtNode), POINTER(AtUniverse)]
_AiNodeGetProcessedGeometry.restype = c_void_p

def AiNodeGetProcessedGeometry(node, dest_universe):
    return NullToNone(_AiNodeGetProcessedGeometry(node, dest_universe), POINTER(AtNode))

# Parameter Writers
#
AiNodeSetByte = ai.AiNodeSetByte
AiNodeSetByte.argtypes = [POINTER(AtNode), AtString, c_ubyte]
AiNodeSetByte.restype = None

AiNodeSetInt = ai.AiNodeSetInt
AiNodeSetInt.argtypes = [POINTER(AtNode), AtString, c_int]
AiNodeSetInt.restype = None

AiNodeSetUInt = ai.AiNodeSetUInt
AiNodeSetUInt.argtypes = [POINTER(AtNode), AtString, c_uint]
AiNodeSetUInt.restype = None

AiNodeSetBool = ai.AiNodeSetBool
AiNodeSetBool.argtypes = [POINTER(AtNode), AtString, c_bool]
AiNodeSetBool.restype = None

AiNodeSetFlt = ai.AiNodeSetFlt
AiNodeSetFlt.argtypes = [POINTER(AtNode), AtString, c_float]
AiNodeSetFlt.restype = None

AiNodeSetRGB = ai.AiNodeSetRGB
AiNodeSetRGB.argtypes = [POINTER(AtNode), AtString, c_float, c_float, c_float]
AiNodeSetRGB.restype = None

AiNodeSetRGBA = ai.AiNodeSetRGBA
AiNodeSetRGBA.argtypes = [POINTER(AtNode), AtString, c_float, c_float, c_float, c_float]
AiNodeSetRGBA.restype = None

AiNodeSetVec = ai.AiNodeSetVec
AiNodeSetVec.argtypes = [POINTER(AtNode), AtString, c_float, c_float, c_float]
AiNodeSetVec.restype = None

AiNodeSetVec2 = ai.AiNodeSetVec2
AiNodeSetVec2.argtypes = [POINTER(AtNode), AtString, c_float, c_float]
AiNodeSetVec2.restype = None

AiNodeSetStr = ai.AiNodeSetStr
AiNodeSetStr.argtypes = [POINTER(AtNode), AtString, AtString]
AiNodeSetStr.restype = None

AiNodeSetPtr = ai.AiNodeSetPtr
AiNodeSetPtr.argtypes = [POINTER(AtNode), AtString, c_void_p]
AiNodeSetPtr.restype = None

AiNodeSetArray = ai.AiNodeSetArray
AiNodeSetArray.argtypes = [POINTER(AtNode), AtString, POINTER(AtArray)]
AiNodeSetArray.restype = None

AiNodeSetMatrix = ai.AiNodeSetMatrix
AiNodeSetMatrix.argtypes = [POINTER(AtNode), AtString, AtMatrix]
AiNodeSetMatrix.restype = None

# Parameter Readers
#

AiNodeGetByte = ai.AiNodeGetByte
AiNodeGetByte.argtypes = [POINTER(AtNode), AtString]
AiNodeGetByte.restype = c_ubyte

AiNodeGetInt = ai.AiNodeGetInt
AiNodeGetInt.argtypes = [POINTER(AtNode), AtString]
AiNodeGetInt.restype = c_int

AiNodeGetUInt = ai.AiNodeGetUInt
AiNodeGetUInt.argtypes = [POINTER(AtNode), AtString]
AiNodeGetUInt.restype = c_uint

AiNodeGetBool = ai.AiNodeGetBool
AiNodeGetBool.argtypes = [POINTER(AtNode), AtString]
AiNodeGetBool.restype = c_bool

AiNodeGetFlt = ai.AiNodeGetFlt
AiNodeGetFlt.argtypes = [POINTER(AtNode), AtString]
AiNodeGetFlt.restype = c_float

AiNodeGetRGB = ai.AiNodeGetRGB
AiNodeGetRGB.argtypes = [POINTER(AtNode), AtString]
AiNodeGetRGB.restype = AtRGB

AiNodeGetRGBA = ai.AiNodeGetRGBA
AiNodeGetRGBA.argtypes = [POINTER(AtNode), AtString]
AiNodeGetRGBA.restype = AtRGBA

AiNodeGetVec = ai.AiNodeGetVec
AiNodeGetVec.argtypes = [POINTER(AtNode), AtString]
AiNodeGetVec.restype = AtVector

_AiNodeGetVec2 = ai.AiNodeGetVec2
_AiNodeGetVec2.argtypes = [POINTER(AtNode), AtString]
if return_small_struct_exception:
    _AiNodeGetVec2.restype = AtVector
    def AiNodeGetVec2(node, param):
        tmp = _AiNodeGetVec2(node, param)
        return AtVector2(tmp.x, tmp.y)
else:
    _AiNodeGetVec2.restype = AtVector2
    AiNodeGetVec2 = _AiNodeGetVec2

_AiNodeGetStr = ai.AiNodeGetStr
_AiNodeGetStr.argtypes = [POINTER(AtNode), AtString]
_AiNodeGetStr.restype = AtStringReturn

def AiNodeGetStr(node, param):
    return AtStringToStr(_AiNodeGetStr(node, param))

_AiNodeGetPtr = ai.AiNodeGetPtr
_AiNodeGetPtr.argtypes = [POINTER(AtNode), AtString]
_AiNodeGetPtr.restype = c_void_p

def AiNodeGetPtr(node, param):
    return NullToNone(_AiNodeGetPtr(node, param), POINTER(AtNode))

_AiNodeGetArray = ai.AiNodeGetArray
_AiNodeGetArray.argtypes = [POINTER(AtNode), AtString]
_AiNodeGetArray.restype = c_void_p

def AiNodeGetArray(node, param):
    return NullToNone(_AiNodeGetArray(node, param), POINTER(AtArray))

AiNodeGetMatrix = ai.AiNodeGetMatrix
AiNodeGetMatrix.argtypes = [POINTER(AtNode), AtString]
AiNodeGetMatrix.restype = AtMatrix

AiNodeSetAttributes = ai.AiNodeSetAttributes
AiNodeSetAttributes.argtypes = [POINTER(AtNode), AtPythonString]
AiNodeSetAttributes.restype = None

AiNodeSetDisabled = ai.AiNodeSetDisabled
AiNodeSetDisabled.argtypes = [POINTER(AtNode), c_bool]
AiNodeSetDisabled.restype = None

AiNodeIsDisabled = ai.AiNodeIsDisabled
AiNodeIsDisabled.argtypes = [POINTER(AtNode)]
AiNodeIsDisabled.restype = c_bool

_AiNodeGetUniverse = ai.AiNodeGetUniverse
_AiNodeGetUniverse.argtypes = [POINTER(AtNode)]
_AiNodeGetUniverse.restype = c_void_p

def AiNodeGetUniverse(node):
    return NullToNone(_AiNodeGetUniverse(node), POINTER(AtUniverse))

_AiNodeGetParent = ai.AiNodeGetParent
_AiNodeGetParent.argtypes = [POINTER(AtNode)]
_AiNodeGetParent.restype = c_void_p

def AiNodeGetParent(node):
    return NullToNone(_AiNodeGetParent(node), POINTER(AtNode))

