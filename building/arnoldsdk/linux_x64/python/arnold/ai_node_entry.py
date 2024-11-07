# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_deprecated import *
from .ai_types import *
from .ai_params import *

# Node types
#
AI_NODE_UNDEFINED =     0x0000  ## Undefined type
AI_NODE_OPTIONS =       0x0001  ## Options node (following the "singleton" pattern, there is only one options node)
AI_NODE_CAMERA =        0x0002  ## Camera nodes (\c persp_camera, \c fisheye_camera, etc)
AI_NODE_LIGHT =         0x0004  ## Light source nodes (\c spot_light, etc)
AI_NODE_SHAPE =         0x0008  ## Geometry nodes (\c sphere, \c polymesh, etc)
AI_NODE_SHADER =        0x0010  ## Shader nodes (\c lambert, etc)
AI_NODE_OVERRIDE =      0x0020  ## EXPERIMENTAL: override nodes support "delayed parameter overrides" for \c procedural nodes
AI_NODE_DRIVER =        0x0040  ## Output driver nodes (\c driver_tiff, etc)
AI_NODE_FILTER =        0x0080  ## Pixel sample filter nodes (\c box_filter, etc
AI_NODE_COLOR_MANAGER = 0x0800  ## Color manager nodes
AI_NODE_OPERATOR =      0x1000  ## Operator plug-in nodes
AI_NODE_IMAGER =        0x2000  ## Imager nodes (\c imager_tonemap, etc */
AI_NODE_ALL =           0xFFFF  ## Bitmask including all node types, used by AiASSWrite()

# Derived Node types
#
AI_NODE_SHAPE_PROCEDURAL = 0x0100  ## Procedural shape node
AI_NODE_SHAPE_VOLUME =     0x0200  ## Volume shape node
AI_NODE_SHAPE_IMPLICIT =   0x0400  ## Implicit shape node

class AtNodeEntry(Structure):
    pass

class AtNodeMethods(Structure):
    pass

class AtParamIterator(Structure):
    pass

class AtMetaDataIterator(Structure):
    pass

class AtMetaDataEntry(Structure):
    _fields_ = [("name", AtStringStruct),
                ("param", AtStringStruct),
                ("type", c_ubyte),
                ("value", AtParamValue)]

_AiNodeEntryLookUp = ai.AiNodeEntryLookUp
_AiNodeEntryLookUp.argtypes = [AtString]
_AiNodeEntryLookUp.restype = c_void_p

def AiNodeEntryLookUp(name):
    return NullToNone(_AiNodeEntryLookUp(name), POINTER(AtNodeEntry))

_AiNodeEntryGetName = ai.AiNodeEntryGetName
_AiNodeEntryGetName.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetName.restype = AtPythonString

def AiNodeEntryGetName(node_entry):
    return AtPythonStringToStr(_AiNodeEntryGetName(node_entry))

AiNodeEntryGetType = ai.AiNodeEntryGetType
AiNodeEntryGetType.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetType.restype = c_int

_AiNodeEntryGetTypeName = ai.AiNodeEntryGetTypeName
_AiNodeEntryGetTypeName.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetTypeName.restype = AtPythonString

def AiNodeEntryGetTypeName(node_entry):
    return AtPythonStringToStr(_AiNodeEntryGetTypeName(node_entry))

AiNodeEntryGetDerivedType = ai.AiNodeEntryGetDerivedType
AiNodeEntryGetDerivedType.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetDerivedType.restype = c_int

_AiNodeEntryGetDerivedTypeName = ai.AiNodeEntryGetDerivedTypeName
_AiNodeEntryGetDerivedTypeName.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetDerivedTypeName.restype = AtPythonString

def AiNodeEntryGetDerivedTypeName(node_entry):
    return AtPythonStringToStr(_AiNodeEntryGetDerivedTypeName(node_entry))

AiNodeEntryGetOutputType = ai.AiNodeEntryGetOutputType
AiNodeEntryGetOutputType.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetOutputType.restype = c_int

_AiNodeEntryGetFilename = ai.AiNodeEntryGetFilename
_AiNodeEntryGetFilename.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetFilename.restype = c_void_p

def AiNodeEntryGetFilename(name):
    return NullToNone(_AiNodeEntryGetFilename(name), AtPythonString)

_AiNodeEntryGetVersion = ai.AiNodeEntryGetVersion
_AiNodeEntryGetVersion.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetVersion.restype = AtPythonString

def AiNodeEntryGetVersion(node_entry):
    return AtPythonStringToStr(_AiNodeEntryGetVersion(node_entry))

AiNodeEntryGetCount = ai.AiNodeEntryGetCount
AiNodeEntryGetCount.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetCount.restype = c_int

AiNodeEntryGetNumParams = ai.AiNodeEntryGetNumParams
AiNodeEntryGetNumParams.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetNumParams.restype = c_int

_AiNodeEntryGetParameter = ai.AiNodeEntryGetParameter
_AiNodeEntryGetParameter.argtypes = [POINTER(AtNodeEntry), c_int]
_AiNodeEntryGetParameter.restype = c_void_p

def AiNodeEntryGetParameter(nentry, index):
    return NullToNone(_AiNodeEntryGetParameter(nentry, index), POINTER(AtParamEntry))

_AiNodeEntryLookUpParameter = ai.AiNodeEntryLookUpParameter
_AiNodeEntryLookUpParameter.argtypes = [POINTER(AtNodeEntry), AtString]
_AiNodeEntryLookUpParameter.restype = c_void_p

def AiNodeEntryLookUpParameter(nentry, name):
    return NullToNone(_AiNodeEntryLookUpParameter(nentry, name), POINTER(AtParamEntry))

AiNodeEntryGetNumOutputs = ai.AiNodeEntryGetNumOutputs
AiNodeEntryGetNumOutputs.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetNumOutputs.restype = c_int

_AiNodeEntryGetOutput = ai.AiNodeEntryGetOutput
_AiNodeEntryGetOutput.argtypes = [POINTER(AtNodeEntry), c_int]
_AiNodeEntryGetOutput.restype = c_void_p

def AiNodeEntryGetOutput(nentry, index):
    return NullToNone(_AiNodeEntryGetOutput(nentry, index), POINTER(AtParamEntry))

_AiNodeEntryLookUpOutput = ai.AiNodeEntryLookUpOutput
_AiNodeEntryLookUpOutput.argtypes = [POINTER(AtNodeEntry), AtString]
_AiNodeEntryLookUpOutput.restype = c_void_p

def AiNodeEntryLookUpOutput(nentry, name):
    return NullToNone(_AiNodeEntryLookUpOutput(nentry, name), POINTER(AtParamEntry))

AiNodeEntryInstall = ai.AiNodeEntryInstall
AiNodeEntryInstall.argtypes = [c_int, c_ubyte, AtPythonString, AtPythonString, POINTER(AtNodeMethods), AtPythonString]
AiNodeEntryInstall.restype = None

AiNodeEntryUninstall = ai.AiNodeEntryUninstall
AiNodeEntryUninstall.argtypes = [AtPythonString]
AiNodeEntryUninstall.restype = None

@deprecated
def AiNodeInstall(type, output_type, name, filename, methods, version):
    return AiNodeEntryInstall(type, output_type, name, filename, methods, version)

@deprecated
def AiNodeUninstall(name):
    return AiNodeEntryUninstall(name)

_AiNodeEntryGetParamIterator = ai.AiNodeEntryGetParamIterator
_AiNodeEntryGetParamIterator.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetParamIterator.restype = c_void_p

def AiNodeEntryGetParamIterator(nentry):
    return NullToNone(_AiNodeEntryGetParamIterator(nentry), POINTER(AtParamIterator))

_AiNodeEntryGetMetaDataIterator = ai.AiNodeEntryGetMetaDataIterator
_AiNodeEntryGetMetaDataIterator.argtypes = [POINTER(AtNodeEntry), AtPythonString]
_AiNodeEntryGetMetaDataIterator.restype = c_void_p

def AiNodeEntryGetMetaDataIterator(nentry, param = None):
    return NullToNone(_AiNodeEntryGetMetaDataIterator(nentry, param), POINTER(AtMetaDataIterator))

AiParamIteratorDestroy = ai.AiParamIteratorDestroy
AiParamIteratorDestroy.argtypes = [POINTER(AtParamIterator)]
AiParamIteratorDestroy.restype = None

_AiParamIteratorGetNext = ai.AiParamIteratorGetNext
_AiParamIteratorGetNext.argtypes = [POINTER(AtParamIterator)]
_AiParamIteratorGetNext.restype = c_void_p

def AiParamIteratorGetNext(iter):
    return NullToNone(_AiParamIteratorGetNext(iter), POINTER(AtParamEntry))

AiParamIteratorFinished = ai.AiParamIteratorFinished
AiParamIteratorFinished.argtypes = [POINTER(AtParamIterator)]
AiParamIteratorFinished.restype = c_bool

AiMetaDataIteratorDestroy = ai.AiMetaDataIteratorDestroy
AiMetaDataIteratorDestroy.argtypes = [POINTER(AtMetaDataIterator)]
AiMetaDataIteratorDestroy.restype = None

_AiMetaDataIteratorGetNext = ai.AiMetaDataIteratorGetNext
_AiMetaDataIteratorGetNext.argtypes = [POINTER(AtMetaDataIterator)]
_AiMetaDataIteratorGetNext.restype = c_void_p

def AiMetaDataIteratorGetNext(iter):
    return NullToNone(_AiMetaDataIteratorGetNext(iter), POINTER(AtMetaDataEntry))

AiMetaDataIteratorFinished = ai.AiMetaDataIteratorFinished
AiMetaDataIteratorFinished.argtypes = [POINTER(AtMetaDataIterator)]
AiMetaDataIteratorFinished.restype = c_bool
