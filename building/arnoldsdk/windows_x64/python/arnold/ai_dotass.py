# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_metadata import AtMetadataStore
from .ai_node_entry import *
from .ai_universe import AtUniverse
from .ai_deprecated import *

@deprecated
def AiASSWrite(universe, filename, mask = AI_NODE_ALL, open_procs = False, binary = True):
    func = ai.AiASSWrite
    func.argtypes = [POINTER(AtUniverse), AtPythonString, c_int, c_bool, c_bool]
    func.restype = c_int

    return func(universe, filename, mask, open_procs, binary)

@deprecated
def AiASSWriteWithMetadata(universe, filename, mask = AI_NODE_ALL, open_procs = False, binary = True, mds = None):
    func = ai.AiASSWriteWithMetadata
    func.argtypes = [POINTER(AtUniverse), AtPythonString, c_int, c_bool, c_bool, POINTER(AtMetadataStore)]
    func.restype = c_int

    return func(universe, filename, mask, open_procs, binary, mds)

@deprecated
def AiASSLoad(universe, filename, mask = AI_NODE_ALL):
    func = ai.AiASSLoad
    func.argtypes = [POINTER(AtUniverse), AtPythonString, c_int]
    func.restype = c_int

    return func(universe, filename, mask)
