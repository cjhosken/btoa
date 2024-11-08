# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_bbox import *
from .ai_types import *
from .ai_node_entry import *
from .ai_nodes import *

class AtChannelLayout(Structure):
   _fields_ = [("channel_type", c_char),
               ("type", c_char),
               ("x_stride", c_size_t),
               ("y_stride", c_size_t)]

AiColorManagerTransformFunc = ai.AiColorManagerTransform
AiColorManagerTransformFunc.argtypes = [POINTER(AtNode), AtString,
                                        c_bool, c_bool, POINTER(AtBBox2),
                                        c_void_p, POINTER(AtChannelLayout),
                                        c_void_p, POINTER(AtChannelLayout)]
AiColorManagerTransformFunc.restype = c_bool

def AiColorManagerTransform(node, name, color, is_output = True) :
   rgb = (c_float * 3)(color[0], color[1], color[2])
   res = AiColorManagerTransformFunc(node, name, c_bool(is_output), False,
                                     None,
                                     pointer(rgb), None, None, None)
   return (rgb[0], rgb[1], rgb[2]) if res else None


AiColorManagerGetDefaultsFunc = ai.AiColorManagerGetDefaults
AiColorManagerGetDefaultsFunc.argtypes = [POINTER(AtNode), POINTER(AtString), POINTER(AtString)]
AiColorManagerGetDefaultsFunc.restype = None

def AiColorManagerGetDefaults(node) :
   linear = AtString()
   sRGB = AtString()
   AiColorManagerGetDefaultsFunc(node, byref(sRGB), byref(linear))
   return (sRGB.value, linear.value)


AiColorManagerGetChromaticitiesFunc = ai.AiColorManagerGetChromaticities
AiColorManagerGetChromaticitiesFunc.argtypes = [POINTER(AtNode), AtString, POINTER(c_float * 8)]
AiColorManagerGetChromaticitiesFunc.restype = c_bool

def AiColorManagerGetChromaticities(node, space) :
   Chromaticities = c_float * 8
   chromaticities = Chromaticities(0, 0, 0, 0, 0, 0, 0, 0)
   res = c_bool(0)
   res = AiColorManagerGetChromaticitiesFunc(node, space, pointer(chromaticities))
   return [ chromaticities[i] for i in range(0, 8) ] if res else None


AiColorManagerGetCustomAttributesFunc = ai.AiColorManagerGetCustomAttributes
AiColorManagerGetCustomAttributesFunc.argtypes = [POINTER(AtNode), AtString, POINTER(c_int), POINTER(c_char_p)]
AiColorManagerGetCustomAttributesFunc.restype = None

def AiColorManagerGetCustomAttributes(node, space) :
   num = c_int(0)
   data = c_char_p(0)
   AiColorManagerGetCustomAttributesFunc(node, space, byref(num), byref(data))
   return [data[i].value for i in range(0, num.value)]


AiColorManagerGetNumColorSpacesFunc = ai.AiColorManagerGetNumColorSpaces
AiColorManagerGetNumColorSpacesFunc.argtypes = [POINTER(AtNode), AtString]
AiColorManagerGetNumColorSpacesFunc.restype = c_int

def AiColorManagerGetNumColorSpaces(node, family = None) :
   return AiColorManagerGetNumColorSpacesFunc(node, family)


AiColorManagerGetColorSpaceNameByIndexFunc = ai.AiColorManagerGetColorSpaceNameByIndex
AiColorManagerGetColorSpaceNameByIndexFunc.argtypes = [POINTER(AtNode), c_int, AtString]
AiColorManagerGetColorSpaceNameByIndexFunc.restype = AtStringReturn

def AiColorManagerGetColorSpaceNameByIndex(node, i, family = None) :
   return AtStringToStr(AiColorManagerGetColorSpaceNameByIndexFunc(node, i, family))


AiColorManagerGetNumFamiliesFunc = ai.AiColorManagerGetNumFamilies
AiColorManagerGetNumFamiliesFunc.argtypes = [POINTER(AtNode)]
AiColorManagerGetNumFamiliesFunc.restype = c_int

def AiColorManagerGetNumFamilies(node) :
   return AiColorManagerGetNumFamiliesFunc(node)


AiColorManagerGetFamilyNameByIndexFunc = ai.AiColorManagerGetFamilyNameByIndex
AiColorManagerGetFamilyNameByIndexFunc.argtypes = [POINTER(AtNode), c_int]
AiColorManagerGetFamilyNameByIndexFunc.restype = AtStringReturn

def AiColorManagerGetFamilyNameByIndex(node, i) :
   return AtStringToStr(AiColorManagerGetFamilyNameByIndexFunc(node, i))


AiColorManagerColorSpaceIsLinearFunc = ai.AiColorManagerColorSpaceIsLinear
AiColorManagerColorSpaceIsLinearFunc.argtypes = [POINTER(AtNode), AtString]
AiColorManagerColorSpaceIsLinearFunc.restype = c_bool

def AiColorManagerColorSpaceIsLinear(node, cs) :
   return AiColorManagerColorSpaceIsLinearFunc(node, cs)
