# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone, AtNode
from .ai_deprecated import *
from .ai_map import AtParamValueMap
from .ai_node_entry import AtNodeEntry, AI_NODE_ALL
from .ai_bbox import *
from .ai_types import *
import warnings

# Cache types
#
AI_CACHE_TEXTURE      = 0x0001  ## Flushes all texturemaps
AI_CACHE_BACKGROUND   = 0x0002  ## Flushes all skydome importance tables for background
AI_CACHE_QUAD         = 0x0004  ## Flushes all quad lights importance tables
AI_CACHE_ALL          = 0xFFFF  ## Flushes all cache types simultaneously

class AtUniverse(Structure):
    pass

class AtNodeIterator(Structure):
    pass

class AtNodeEntryIterator(Structure):
    pass

class AtAOVIterator(Structure):
    pass

class AtAOVEntry(Structure):
    _fields_ = [("name", AtStringStruct),
                ("type", c_ubyte),
                ("blend_mode", c_int),
                ("expression", AtStringStruct)]

_AiUniverse = ai.AiUniverse
_AiUniverse.argtypes = []
_AiUniverse.restype = c_void_p

def AiUniverse():
    return NullToNone(_AiUniverse(), POINTER(AtUniverse))

AiUniverseDestroy = ai.AiUniverseDestroy
AiUniverseDestroy.argtypes = [POINTER(AtUniverse)]
AiUniverseDestroy.restype = None

@deprecated
def AiUniverseIsActive():
    func = ai.AiUniverseIsActive
    func.argtypes = []
    func.restype = c_bool
    return func()

AiUniverseCacheFlush = ai.AiUniverseCacheFlush
AiUniverseCacheFlush.argtypes = [POINTER(AtUniverse), c_int]
AiUniverseCacheFlush.restype = None

def AiUniverseGetOptions(universe):
    func = ai.AiUniverseGetOptions
    func.argtypes = [POINTER(AtUniverse)]
    func.restype = c_void_p
    return NullToNone(func(universe), POINTER(AtNode))

def AiUniverseGetCamera(universe):
    func = ai.AiUniverseGetCamera
    func.argtypes = [POINTER(AtUniverse)]
    func.restype = c_void_p
    return NullToNone(func(universe), POINTER(AtNode))

AiUniverseGetSceneBounds = ai.AiUniverseGetSceneBounds
AiUniverseGetSceneBounds.argtypes = [POINTER(AtUniverse)]
AiUniverseGetSceneBounds.restype = AtBBox

def AiUniverseGetNodeIterator(universe, mask):
    func = ai.AiUniverseGetNodeIterator
    func.argtypes = [POINTER(AtUniverse), c_uint]
    func.restype = c_void_p
    return NullToNone(func(universe, mask), POINTER(AtNodeIterator))

def AiUniverseGetNodeEntryIterator(mask):
    func = ai.AiUniverseGetNodeEntryIterator
    func.argtypes = [c_uint]
    func.restype = c_void_p

    return NullToNone(func(mask), POINTER(AtNodeEntryIterator))

def AiUniverseGetAOVIterator(universe):
    func = ai.AiUniverseGetAOVIterator
    func.argtypes = []
    func.restype = c_void_p
    return NullToNone(func(universe), POINTER(AtAOVIterator))

AiUniverseAddDefaultNodes = ai.AiUniverseAddDefaultNodes
AiUniverseAddDefaultNodes.argtypes = [POINTER(AtUniverse), POINTER(AtParamValueMap)]
AiUniverseAddDefaultNodes.restype = None

def AiUniverseCompare(universe1, universe2, node_mask = AI_NODE_ALL, diffs = None):
    func = ai.AiUniverseCompare
    func.argtypes = [POINTER(AtUniverse), POINTER(AtUniverse), c_uint, POINTER(AtParamValueMap)]
    func.restype = c_bool

    return func(universe1, universe2, node_mask, diffs)

AiUniverseGetId = ai.AiUniverseGetId
AiUniverseGetId.argtypes = [POINTER(AtUniverse)]
AiUniverseGetId.restype = c_uint

def AiUniverseGetFromId(universe_id):
    func = ai.AiUniverseGetFromId
    func.argtypes = [c_uint]
    func.restype = POINTER(AtUniverse)

    return NullToNone(func(universe_id), POINTER(AtUniverse))

AiNodeIteratorDestroy = ai.AiNodeIteratorDestroy
AiNodeIteratorDestroy.argtypes = [POINTER(AtNodeIterator)]
AiNodeIteratorDestroy.restype = None

def AiNodeIteratorGetNext(iter):
    func = ai.AiNodeIteratorGetNext
    func.argtypes = [POINTER(AtNodeIterator)]
    func.restype = c_void_p

    return NullToNone(func(iter), POINTER(AtNode))

AiNodeIteratorFinished = ai.AiNodeIteratorFinished
AiNodeIteratorFinished.argtypes = [POINTER(AtNodeIterator)]
AiNodeIteratorFinished.restype = c_bool

AiNodeEntryIteratorDestroy = ai.AiNodeEntryIteratorDestroy
AiNodeEntryIteratorDestroy.argtypes = [POINTER(AtNodeEntryIterator)]
AiNodeEntryIteratorDestroy.restype = None

def AiNodeEntryIteratorGetNext(iter):
    func = ai.AiNodeEntryIteratorGetNext
    func.argtypes = [POINTER(AtNodeEntryIterator)]
    func.restype = c_void_p

    return NullToNone(func(iter), POINTER(AtNodeEntry))

AiNodeEntryIteratorFinished = ai.AiNodeEntryIteratorFinished
AiNodeEntryIteratorFinished.argtypes = [POINTER(AtNodeEntryIterator)]
AiNodeEntryIteratorFinished.restype = c_bool

AiAOVIteratorDestroy = ai.AiAOVIteratorDestroy
AiAOVIteratorDestroy.argtypes = [POINTER(AtAOVIterator)]
AiAOVIteratorDestroy.restype = None

def AiAOVIteratorGetNext(iter):
    func = ai.AiAOVIteratorGetNext
    func.argtypes = [POINTER(AtAOVIterator)]
    func.restype = c_void_p

    return NullToNone(func(iter), POINTER(AtAOVEntry))

AiAOVIteratorFinished = ai.AiAOVIteratorFinished
AiAOVIteratorFinished.argtypes = [POINTER(AtAOVIterator)]
AiAOVIteratorFinished.restype = c_bool
