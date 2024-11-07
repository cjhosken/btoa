# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_types import *
from .ai_nodes import *
from .ai_materialx import *
from .ai_map import *

AiMaterialxWriteFunc = ai.AiMaterialxWrite
AiMaterialxWriteFunc.argtypes = [POINTER(AtUniverse), AtPythonString, AtPythonString, AtPythonString, c_bool]
AiMaterialxWriteFunc.restype = c_int

def AiMaterialxWrite(universe, filename, look_name, properties="", relative=True):
    return AiMaterialxWriteFunc(universe, filename, look_name, properties, relative)

AiMaterialxWriteMaterialFunc = ai.AiMaterialxWriteMaterial
AiMaterialxWriteMaterialFunc.argtypes = [AtPythonString, AtPythonString, POINTER(AtNode), POINTER(AtNode), POINTER(AtNode)]
AiMaterialxWriteMaterialFunc.restype = c_int

def AiMaterialxWriteMaterial(filename, material_name, surface=None, volume=None, displacement=None):
    return AiMaterialxWriteMaterialFunc(filename, material_name, surface, volume, displacement)

AiMaterialxGetLookNames = ai.AiMaterialxGetLookNames
AiMaterialxGetLookNames.argtypes = [AtPythonString]
AiMaterialxGetLookNames.restype = POINTER(AtArray)

AiMaterialxGetMaterialNames = ai.AiMaterialxGetMaterialNames
AiMaterialxGetMaterialNames.argtypes = [AtPythonString]
AiMaterialxGetMaterialNames.restype = POINTER(AtArray)

AiMaterialxReadMaterialsFunc = ai.AiMaterialxReadMaterials
AiMaterialxReadMaterialsFunc.argtypes = [POINTER(AtUniverse), AtPythonString, POINTER(AtParamValueMap), POINTER(AtArray)]
AiMaterialxReadMaterialsFunc.restype = c_int

def AiMaterialxReadMaterials(universe, filename, params=None, nodes=None):
    return AiMaterialxReadMaterialsFunc(universe, filename, params, nodes)

AiMaterialxGetOslShaderCodeFunc = ai.AiMaterialxGetOslShaderCode
AiMaterialxGetOslShaderCodeFunc.argtypes = [AtPythonString, AtPythonString, POINTER(AtParamValueMap)]
AiMaterialxGetOslShaderCodeFunc.restype = AtStringReturn

def AiMaterialxGetOslShaderCode(node_definition, shader_name, connected_inputs=None):
    return AtStringToStr(AiMaterialxGetOslShaderCodeFunc(node_definition, shader_name, connected_inputs))

AiMaterialxGetNodeEntryFromDefinitionFunc = ai.AiMaterialxGetNodeEntryFromDefinition
AiMaterialxGetNodeEntryFromDefinitionFunc.argtypes = [AtPythonString, POINTER(AtParamValueMap)]
AiMaterialxGetNodeEntryFromDefinitionFunc.restype = c_void_p

def AiMaterialxGetNodeEntryFromDefinition(node_definition, optional_parameters=None):
    return NullToNone(AiMaterialxGetNodeEntryFromDefinitionFunc(node_definition, optional_parameters), POINTER(AtNodeEntry))
