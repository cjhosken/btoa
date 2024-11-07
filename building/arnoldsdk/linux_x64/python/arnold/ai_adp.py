# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_map import *


AI_ADP_HOSTNAME      = "ADDIN_PARENT_NAME"
AI_ADP_HOSTVERSION   = "ADDIN_PARENT_VERSION"
AI_ADP_PLUGINNAME    = "ADDIN_NAME"
AI_ADP_PLUGINVERSION = "ADDIN_VERSION"

AI_ADP_DIALOG_ONLY_FIRST_TIME = 1
AI_ADP_DIALOG_ALWAYS = 2

def AiADPDisplayDialogWindow(mode = AI_ADP_DIALOG_ALWAYS):
    func = ai.AiADPDisplayDialogWindow
    func.argtypes = [c_int]
    func.restype = None
    return func(mode)

AiADPDisableDialogWindow = ai.AiADPDisableDialogWindow
AiADPDisableDialogWindow.restype = None

AiADPSetOptedIn = ai.AiADPSetOptedIn
AiADPSetOptedIn.argtypes = [c_bool]
AiADPSetOptedIn.restype = None

AiADPIsOptedIn = ai.AiADPIsOptedIn
AiADPIsOptedIn.restype = c_bool

AiADPAddProductMetadata = ai.AiADPAddProductMetadata
AiADPAddProductMetadata.argtypes = [AtString, AtString]
AiADPAddProductMetadata.restype = None
