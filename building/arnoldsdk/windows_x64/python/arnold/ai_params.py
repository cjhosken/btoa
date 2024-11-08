# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_matrix import *
from .ai_array import *
from .ai_enum import *
from .ai_color import *
from .ai_vector import *
from .ai_types import *

# Parameter types
#
AI_TYPE_BYTE =          0x00  ## Byte (an 8-bit sized unsigned integer)
AI_TYPE_INT =           0x01  ## Integer
AI_TYPE_UINT =          0x02  ## Unsigned integer
AI_TYPE_BOOLEAN =       0x03  ## Boolean (either TRUE or FALSE)
AI_TYPE_FLOAT =         0x04  ## Single-precision floating point number
AI_TYPE_RGB =           0x05  ## RGB struct
AI_TYPE_RGBA =          0x06  ## RGBA struct
AI_TYPE_VECTOR =        0x07  ## XYZ vector
AI_TYPE_VECTOR2 =       0x09  ## XY point
AI_TYPE_STRING =        0x0A  ## C-style character string
AI_TYPE_POINTER =       0x0B  ## Arbitrary pointer
AI_TYPE_NODE =          0x0C  ## Pointer to an Arnold node
AI_TYPE_ARRAY =         0x0D  ## AtArray
AI_TYPE_MATRIX =        0x0E  ## 4x4 matrix
AI_TYPE_ENUM =          0x0F  ## Enumeration (see \ref AtEnum)
AI_TYPE_CLOSURE =       0x10  ## Shader closure
AI_TYPE_USHORT =        0x11  ## unsigned short (16-bit unsigned integer) (used by drivers only)
AI_TYPE_HALF =          0x12  ## 16-bit, half-precision float (used by drivers only)
AI_TYPE_UNDEFINED =     0xFF  ## Undefined, you should never encounter a parameter of this type
AI_TYPE_NONE =          0xFF  ## No type

# Parameter categories
#
AI_USERDEF_UNDEFINED = 0  ## Undefined, you should never encounter a parameter of this category
AI_USERDEF_CONSTANT =  1  ## User-defined: per-object parameter
AI_USERDEF_UNIFORM =   2  ## User-defined: per-face parameter
AI_USERDEF_VARYING =   3  ## User-defined: per-vertex parameter
AI_USERDEF_INDEXED =   4  ## User-defined: per-face-vertex parameter

class AtParamValue(Union):
    _fields_ = [("BYTE",  c_ubyte),
                ("INT",   c_int),
                ("UINT",  c_uint),
                ("BOOL",  c_bool),
                ("FLT",   c_float),
                ("RGB",   AtRGB),
                ("RGBA",  AtRGBA),
                ("VEC",   AtVector),
                ("VEC2",  AtVector2),
                ("STR",   AtStringStruct),
                ("PTR",   c_void_p),
                ("ARRAY", POINTER(AtArray)),
                ("pMTX",  POINTER(AtMatrix))]

class AtParamEntry(Structure):
    pass

_AiParamGetName = ai.AiParamGetName
_AiParamGetName.argtypes = [POINTER(AtParamEntry)]
_AiParamGetName.restype = AtStringReturn

def AiParamGetName(param_entry):
    return AtStringToStr(_AiParamGetName(param_entry))

AiParamGetType = ai.AiParamGetType
AiParamGetType.argtypes = [POINTER(AtParamEntry)]
AiParamGetType.restype = c_uint8

AiParamGetSubType = ai.AiParamGetSubType
AiParamGetSubType.argtypes = [POINTER(AtParamEntry)]
AiParamGetSubType.restype = c_int

_AiParamGetDefault = ai.AiParamGetDefault
_AiParamGetDefault.argtypes = [POINTER(AtParamEntry)]
_AiParamGetDefault.restype = c_void_p

def AiParamGetDefault(pentry):
    return NullToNone(_AiParamGetDefault(pentry), POINTER(AtParamValue))

AiParamGetEnum = ai.AiParamGetEnum
AiParamGetEnum.argtypes = [POINTER(AtParamEntry)]
AiParamGetEnum.restype = AtEnum

_AiParamGetTypeName = ai.AiParamGetTypeName
_AiParamGetTypeName.argtypes = [c_ubyte]
_AiParamGetTypeName.restype = AtPythonString

def AiParamGetTypeName(index):
    return AtPythonStringToStr(_AiParamGetTypeName(index))

AiParamGetTypeSize = ai.AiParamGetTypeSize
AiParamGetTypeSize.argtypes = [c_ubyte]
AiParamGetTypeSize.restype = c_int

class AtUserParamEntry(Structure):
    pass

_AiUserParamGetName = ai.AiUserParamGetName
_AiUserParamGetName.argtypes = [POINTER(AtUserParamEntry)]
_AiUserParamGetName.restype = AtPythonString

def AiUserParamGetName(user_param_entry):
    return AtPythonStringToStr(_AiUserParamGetName(user_param_entry))

AiUserParamGetType = ai.AiUserParamGetType
AiUserParamGetType.argtypes = [POINTER(AtUserParamEntry)]
AiUserParamGetType.restype = c_int

AiUserParamGetArrayType = ai.AiUserParamGetArrayType
AiUserParamGetArrayType.argtypes = [POINTER(AtUserParamEntry)]
AiUserParamGetArrayType.restype = c_int

AiUserParamGetCategory = ai.AiUserParamGetCategory
AiUserParamGetCategory.argtypes = [POINTER(AtUserParamEntry)]
AiUserParamGetCategory.restype = c_int
