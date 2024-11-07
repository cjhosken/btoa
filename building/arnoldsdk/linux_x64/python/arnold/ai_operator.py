# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_types import *
from .ai_nodes import *
from .ai_operator import *
import warnings

AiOpSetTarget = ai.AiOpSetTarget
AiOpSetTarget.argtypes = [POINTER(AtUniverse), POINTER(AtNode)]
AiOpSetTarget.restype = c_bool

def AiOpGetTarget(universe):
    func = ai.AiOpGetTarget
    func.argtypes = [POINTER(AtUniverse)]
    func.restype = c_void_p
    return NullToNone(func(universe), POINTER(AtNode))

AiOpGetInputs = ai.AiOpGetInputs
AiOpGetInputs.argtypes = [POINTER(AtNode)]
AiOpGetInputs.restype = POINTER(AtArray)

AiOpLinkFunc = ai.AiOpLink
AiOpLinkFunc.argtypes = [POINTER(AtNode), POINTER(AtNode), c_int]
AiOpLinkFunc.restype = c_bool

def AiOpLink(from_node, to_node, index=-1):
    AiOpLinkFunc(from_node, to_node, index)

AiOpUnlink = ai.AiOpUnlink
AiOpUnlink.argtypes = [POINTER(AtNode), POINTER(AtNode)]
AiOpUnlink.restype = c_bool

AiOpUnlinkInputByIndex = ai.AiOpUnlinkInputByIndex
AiOpUnlinkInputByIndex.argtypes = [POINTER(AtNode), c_uint]
AiOpUnlinkInputByIndex.restype = c_bool

AiOpMatchNodeSelectionFunc = ai.AiOpMatchNodeSelection
AiOpMatchNodeSelectionFunc.argtypes = [POINTER(AtNode), AtPythonString, c_bool, POINTER(AtNode)]
AiOpMatchNodeSelectionFunc.restype = c_bool

def AiOpMatchNodeSelection(node, selection, relative=True, target=None):
    return AiOpMatchNodeSelectionFunc(node, selection, relative, target)
