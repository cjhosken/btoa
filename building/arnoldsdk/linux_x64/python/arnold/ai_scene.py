# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_types import *
from .ai_metadata import AtMetadataStore
from .ai_universe import AtUniverse
from .ai_map import AtParamValueMap

class AtSceneFormatIterator(Structure):
    pass

class AtSceneFormatExtensionIterator(Structure):
    pass

class AtSceneFormatData(Structure):
    pass

def _AiSceneLoad(universe, filename, params):
    func = ai.AiSceneLoad
    func.argtypes = [POINTER(AtUniverse), AtPythonString, POINTER(AtParamValueMap)]
    func.restype = c_bool

    return func(universe, filename, params)

def AiSceneLoad(*args):
    return _AiSceneLoad(*args) if args[0] is None or type(args[0]) == POINTER(AtUniverse) else _AiSceneLoad(None, *args)

def _AiSceneWrite(universe, filename, params, mds = None):
    func = ai.AiSceneWrite
    func.argtypes = [POINTER(AtUniverse), AtPythonString, POINTER(AtParamValueMap), POINTER(AtMetadataStore)]
    func.restype = c_bool

    return func(universe, filename, params, mds)

def AiSceneWrite(*args):
    return _AiSceneWrite(*args) if args[0] is None or type(args[0]) == POINTER(AtUniverse) else _AiSceneWrite(None, *args)

def AiSceneFormatSupported(extension):
    func = ai.AiSceneFormatSupported
    func.argtypes = [AtPythonString]
    func.restype = c_bool

    return func(extension)

def AiSceneFormatIterator():
    func = ai.AiSceneFormatIterator
    func.argtypes = []
    func.restype = c_void_p

    return NullToNone(func(), POINTER(AtSceneFormatIterator))

def AiSceneFormatIteratorDestroy(iter):
    func = ai.AiSceneFormatIteratorDestroy
    func.argtypes = [POINTER(AtSceneFormatIterator)]
    func.restype = None

    func(iter)

def AiSceneFormatIteratorGetNext(iter):
    func = ai.AiSceneFormatIteratorGetNext
    func.argtypes = [POINTER(AtSceneFormatIterator)]
    func.restype = POINTER(AtSceneFormatData)

    return NullToNone(func(iter), POINTER(AtSceneFormatData))

def AiSceneFormatIteratorFinished(iter):
    func = ai.AiSceneFormatIteratorFinished
    func.argtypes = [POINTER(AtSceneFormatIterator)]
    func.restype = c_bool

    return func(iter)

def AiSceneFormatGetExtensionIterator(format_data):
    func = ai.AiSceneFormatGetExtensionIterator
    func.argtypes = [POINTER(AtSceneFormatData)]
    func.restype = POINTER(AtSceneFormatExtensionIterator)

    return NullToNone(func(format_data), POINTER(AtSceneFormatExtensionIterator))

def AiSceneFormatExtensionIteratorDestroy(iter):
    func = ai.AiSceneFormatExtensionIteratorDestroy
    func.argtypes = [POINTER(AtSceneFormatExtensionIterator)]
    func.restype = None

    func(iter)

def AiSceneFormatExtensionIteratorGetNext(iter):
    func = ai.AiSceneFormatExtensionIteratorGetNext
    func.argtypes = [POINTER(AtSceneFormatExtensionIterator)]
    func.restype = AtPythonString

    return AtPythonStringToStr(func(iter))

def AiSceneFormatExtensionIteratorFinished(iter):
    func = ai.AiSceneFormatExtensionIteratorFinished
    func.argtypes = [POINTER(AtSceneFormatExtensionIterator)]
    func.restype = c_bool

    return func(iter)

def AiSceneFormatGetName(format_data):
    func = ai.AiSceneFormatGetName
    func.argtypes = [POINTER(AtSceneFormatData)]
    func.restype = AtPythonString

    return AtPythonStringToStr(func(format_data))

def AiSceneFormatGetDescription(format_data):
    func = ai.AiSceneFormatGetDescription
    func.argtypes = [POINTER(AtSceneFormatData)]
    func.restype = AtPythonString

    return AtPythonStringToStr(func(format_data))

def AiSceneFormatSupportsReading(format_data):
    func = ai.AiSceneFormatSupportsReading
    func.argtypes = [POINTER(AtSceneFormatData)]
    func.restype = c_bool

    return func(format_data)

def AiSceneFormatSupportsWriting(format_data):
    func = ai.AiSceneFormatSupportsWriting
    func.argtypes = [POINTER(AtSceneFormatData)]
    func.restype = c_bool

    return func(format_data)

def AiSceneFormatGetMetadataStore(format_data):
    func = ai.AiSceneFormatGetMetadataStore
    func.argtypes = [POINTER(AtSceneFormatData)]
    func.restype = POINTER(AtMetadataStore)

    return NullToNone(func(format_data), POINTER(AtMetadataStore))
