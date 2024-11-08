# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

# TODO: Add callback handling

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_map import *
from .ai_universe import AtUniverse
import warnings

# Severity levels (for callback function)
#
AI_SEVERITY_INFO =      0x00  ## regular information message
AI_SEVERITY_WARNING =   0x01  ## warning message
AI_SEVERITY_ERROR =     0x02  ## error message
AI_SEVERITY_FATAL =     0x03  ## fatal error message

# Logging flags
#
AI_LOG_NONE =          0x0000  ## don't show any messages
AI_LOG_INFO =          0x0001  ## show all regular information messages
AI_LOG_WARNINGS =      0x0002  ## show warning messages
AI_LOG_ERRORS =        0x0004  ## show error messages
AI_LOG_DEBUG =         0x0008  ## show debug messages
AI_LOG_STATS =         0x0010  ## show detailed render statistics
AI_LOG_ASS_PARSE =     0x0020  ## show .ass-file parsing details
AI_LOG_PLUGINS =       0x0040  ## show details about plugins loaded
AI_LOG_PROGRESS =      0x0080  ## show a progress message at 5% increments while rendering
AI_LOG_NAN =           0x0100  ## show warnings for pixels with NaN's
AI_LOG_TIMESTAMP =     0x0200  ## prefix messages with a timestamp (elapsed time)
AI_LOG_BACKTRACE =     0x0400  ## show the stack contents after abnormal program termination (\c SIGSEGV, etc)
AI_LOG_MEMORY =        0x0800  ## prefix messages with current memory usage
AI_LOG_COLOR =         0x1000  ## add colors to log messages based on severity
AI_LOG_ALL = AI_LOG_INFO      | AI_LOG_WARNINGS  | AI_LOG_ERRORS    | \
             AI_LOG_DEBUG     | AI_LOG_STATS     | AI_LOG_PLUGINS   | \
             AI_LOG_PROGRESS  | AI_LOG_NAN       | AI_LOG_ASS_PARSE | \
             AI_LOG_TIMESTAMP | AI_LOG_BACKTRACE | AI_LOG_MEMORY    | \
             AI_LOG_COLOR

AiMsgSetLogFileName = ai.AiMsgSetLogFileName
AiMsgSetLogFileName.argtypes = [AtPythonString]
AiMsgSetLogFileName.restype = None

AiMsgSetLogFileFlags = ai.AiMsgSetLogFileFlags
AiMsgSetLogFileFlags.argtypes = [POINTER(AtUniverse), c_int]
AiMsgSetLogFileFlags.restype = None

AiMsgSetConsoleFlags = ai.AiMsgSetConsoleFlags
AiMsgSetConsoleFlags.argtypes = [POINTER(AtUniverse), c_int]
AiMsgSetConsoleFlags.restype = None

AiMsgSetMaxWarnings = ai.AiMsgSetMaxWarnings
AiMsgSetMaxWarnings.argtypes = [c_int]
AiMsgSetMaxWarnings.restype = None

# Callback function receives the following parameters:
#     int    --> log mask
#     int    --> message severity level
#     string --> message string
#     int    --> tabs
AtMsgCallBack = CFUNCTYPE(None, c_int, c_int, AtPythonString, c_int)

@deprecated
def AiMsgSetCallback(cb):
    # keep a reference to avoid the callback getting garbage collected
    ai.msg_callback_reference = cb

    func = ai.AiMsgSetCallback
    func.argtypes = [AtMsgCallBack]
    func.restype = None
    func(cb)

@deprecated
def AiMsgAddCallback(cb):
    # keep a reference to avoid the callback getting garbage collected
    ai.msg_callback_reference = cb

    func = ai.AiMsgAddCallback
    func.argtypes = [AtMsgCallBack]
    func.restype = None
    func(cb)

@deprecated
def AiMsgResetCallback():
    ai.msg_callback_reference = None

    func = ai.AiMsgResetCallback
    func.argtypes = []
    func.restype = None
    func()

AtMsgExtendedCallBack = CFUNCTYPE(None, c_int, c_int, AtPythonString, POINTER(AtParamValueMap), c_void_p)

def AiMsgRegisterCallback(cb, mask, user):
    ai.msg_registered_callbacks_reference = cb
    func = ai.AiMsgRegisterCallback
    func.argtypes = [AtMsgExtendedCallBack, c_int, c_void_p]
    func.restype = c_int
    return func(cb, mask, user)

def AiMsgDeregisterCallback(id):
    func = ai.AiMsgDeregisterCallback
    func.argtypes = [c_int]
    func.restype = None
    func(id)

def AiMsgSetCallbackMask(id, mask):
    func = ai.AiMsgSetCallbackMask
    func.argtypes = [c_int, c_int]
    func.restype = None
    func(id, mask)

def AiMsgInfo(format, *params):
    func = ai.AiMsgInfo
    func.argtypes = [AtPythonString]
    func.restype = None
    func(format, *params)

def AiMsgDebug(format, *params):
    func = ai.AiMsgDebug
    func.argtypes = [AtPythonString]
    func.restype = None
    func(format, *params)

def AiMsgWarning(format, *params):
    func = ai.AiMsgWarning
    func.argtypes = [AtPythonString]
    func.restype = None
    func(format, *params)

def AiMsgError(format, *params):
    func = ai.AiMsgError
    func.argtypes = [AtPythonString]
    func.restype = None
    func(format, *params)

def AiMsgFatal(format, *params):
    func = ai.AiMsgFatal
    func.argtypes = [AtPythonString]
    func.restype = None
    func(format, *params)

AiMsgTab = ai.AiMsgTab
AiMsgTab.argtypes = [c_int]
AiMsgTab.restype = None

AiMsgUtilGetUsedMemory = ai.AiMsgUtilGetUsedMemory
AiMsgUtilGetUsedMemory.argtypes = []
AiMsgUtilGetUsedMemory.restype = c_uint64

AiMsgUtilGetElapsedTime = ai.AiMsgUtilGetElapsedTime
AiMsgUtilGetElapsedTime.argtypes = []
AiMsgUtilGetElapsedTime.restype = c_uint32

AiMsgSystemInfo = ai.AiMsgSystemInfo
AiMsgSystemInfo.argtypes = [POINTER(AtUniverse)]
AiMsgSystemInfo.restype = None
