# Copyright 2023 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai, NullToNone, AtNode
from .ai_deprecated import *
from .ai_types import *
from .ai_universe import AtUniverse
import warnings

class AtRenderSession(Structure):
    pass

# Rendering modes
#
AtRenderMode = c_int
AI_RENDER_MODE_CAMERA = AtRenderMode(0)  ## Instruct Arnold to render from a camera
AI_RENDER_MODE_FREE =   AtRenderMode(1)  ## Put Arnold in a mode to process arbitrary ray requests

# Error codes
#
AtRenderErrorCode = c_int
AI_SUCCESS =                       AtRenderErrorCode(0)    ## no error
AI_ABORT =                         AtRenderErrorCode(1)    ## render aborted
AI_ERROR_NO_CAMERA =               AtRenderErrorCode(2)    ## camera not defined
AI_ERROR_BAD_CAMERA =              AtRenderErrorCode(3)    ## bad camera data
AI_ERROR_VALIDATION =              AtRenderErrorCode(4)    ## usage not validated
AI_ERROR_RENDER_REGION =           AtRenderErrorCode(5)    ## invalid render region
AI_INTERRUPT =                     AtRenderErrorCode(6)    ## render interrupted by user
AI_ERROR_NO_OUTPUTS =              AtRenderErrorCode(7)    ## no rendering outputs
AI_ERROR_UNAVAILABLE_DEVICE =      AtRenderErrorCode(8)    ## cannot create GPU context
AI_ERROR =                         AtRenderErrorCode(9)    ## generic error

# Session mode
#
AtSessionMode = c_int
AI_SESSION_BATCH       = AtSessionMode(0)  ## batch mode, extra (possibly destructive) optimizations allowed
AI_SESSION_INTERACTIVE = AtSessionMode(1)  ## interactive mode, can read/write nodes after rendering

# Display outputs ready
#
AtDisplayOutput = c_int
AI_DISPLAY_OUTPUT_NONE                = AtDisplayOutput(0)  ## no updates ready; check render status or error code
AI_DISPLAY_OUTPUT_INTERACTIVE         = AtDisplayOutput(1)  ## interactive output updated fully, display on screen
AI_DISPLAY_OUTPUT_PARTIAL_INTERACTIVE = AtDisplayOutput(2)  ## interactive output updated but not the whole image; put on screen anyway
AI_DISPLAY_OUTPUT_ALL                 = AtDisplayOutput(3)  ## all outputs are getting updated, any output can be displayed

# Render status
#
AtRenderStatus = c_int
AI_RENDER_STATUS_NOT_STARTED = AtRenderStatus(0)  ## Before AiRenderBegin(), or after AiRenderEnd()
AI_RENDER_STATUS_PAUSED      = AtRenderStatus(1)  ## Update callback paused the render or AiRenderInterrupt() called
AI_RENDER_STATUS_RESTARTING  = AtRenderStatus(2)  ## Update callback is restarting the render
AI_RENDER_STATUS_RENDERING   = AtRenderStatus(3)  ## Currently actively rendering passes
AI_RENDER_STATUS_FINISHED    = AtRenderStatus(4)  ## Render done, but AiRenderEnd() not called yet
AI_RENDER_STATUS_FAILED      = AtRenderStatus(5)  ## Render failed, AiRenderEnd() will return the actual error code (AtRenderErrorCode)

# Reason for invoking the render update callback
#
AtRenderUpdateType = c_int
AI_RENDER_UPDATE_INTERRUPT   = AtRenderUpdateType(0)  ## Callback invoked after render is interrupted and paused, can change the scene
AI_RENDER_UPDATE_BEFORE_PASS = AtRenderUpdateType(1)  ## Callback invoked just before render pass is to begin, can change the scene
AI_RENDER_UPDATE_DURING_PASS = AtRenderUpdateType(2)  ## Callback invoked during render pass after some pixel data is ready
AI_RENDER_UPDATE_AFTER_PASS  = AtRenderUpdateType(3)  ## Callback invoked after a non-final render pass is done, can change the scene
AI_RENDER_UPDATE_FINISHED    = AtRenderUpdateType(4)  ## Callback invoked after the final render pass is done, can change the scene
AI_RENDER_UPDATE_ERROR       = AtRenderUpdateType(5)  ## Callback invoked when an error or abort occurs, and the render has failed

# System handler mask
#
AtSystemHandlerMask  = c_int
AI_SYSTEM_HANDLER_NONE       = AtSystemHandlerMask(0) ## no handlers will be installed
AI_SYSTEM_HANDLER_ALL        = AtSystemHandlerMask(255) ## all handlers will be installed

# Additional information for render callbacks about the current render pass
#
class AtRenderUpdateInfo(Structure):
    _fields_ = [("render_session", POINTER(AtRenderSession)),
                ("outputs_to_display", AtDisplayOutput),
                ("pass_index", c_uint),
                ("total_passes", c_uint),
                ("current_AA_samples", c_int),
                ("current_AA_samples_max", c_int),
                ("current_GI_diffuse_samples", c_int),
                ("current_GI_specular_samples", c_int),
                ("current_GI_transmission_samples", c_int),
                ("current_GI_sss_samples", c_int),
                ("current_GI_volume_samples", c_int)]

# Render callback signature
#
AtRenderUpdateCallback = CFUNCTYPE(AtRenderStatus, c_void_p, AtRenderUpdateType, POINTER(AtRenderUpdateInfo))

def AiBegin(mode = AI_SESSION_BATCH):
    func = ai.AiBegin
    func.argtypes = [AtSessionMode]
    func.restype = None
    return func(mode)

AiEnd = ai.AiEnd
AiEnd.argtypes = []
AiEnd.restype = None

AiSetSystemHandlers = ai.AiSetSystemHandlers
AiSetSystemHandlers.argtypes = [AtSystemHandlerMask]
AiSetSystemHandlers.restype = None

AiArnoldIsActive = ai.AiArnoldIsActive
AiArnoldIsActive.argtypes = []
AiArnoldIsActive.restype = c_bool

AiGetSessionMode = ai.AiGetSessionMode
AiGetSessionMode.argtypes = [POINTER(AtRenderSession)]
AiGetSessionMode.restype = AtSessionMode

AiRenderAddInteractiveOutput = ai.AiRenderAddInteractiveOutput
AiRenderAddInteractiveOutput.argtypes = [POINTER(AtRenderSession), c_uint]
AiRenderAddInteractiveOutput.restype = None

AiRenderIsInteractiveOutput = ai.AiRenderIsInteractiveOutput
AiRenderIsInteractiveOutput.argtypes = [POINTER(AtRenderSession), c_uint]
AiRenderIsInteractiveOutput.restype = c_bool

AiRenderRemoveInteractiveOutput = ai.AiRenderRemoveInteractiveOutput
AiRenderRemoveInteractiveOutput.argtypes = [POINTER(AtRenderSession), c_uint]
AiRenderRemoveInteractiveOutput.restype = c_bool

AiRenderRemoveAllInteractiveOutputs = ai.AiRenderRemoveAllInteractiveOutputs
AiRenderRemoveAllInteractiveOutputs.argtypes = [POINTER(AtRenderSession)]
AiRenderRemoveAllInteractiveOutputs.restype = None

AiRenderGetHintBool = ai.AiRenderGetHintBool
AiRenderGetHintBool.argtypes = [POINTER(AtRenderSession), AtString, POINTER(c_bool)]
AiRenderGetHintBool.restype = c_bool

AiRenderGetHintInt = ai.AiRenderGetHintInt
AiRenderGetHintInt.argtypes = [POINTER(AtRenderSession), AtString, POINTER(c_int)]
AiRenderGetHintInt.restype = c_bool

AiRenderGetHintFlt = ai.AiRenderGetHintFlt
AiRenderGetHintFlt.argtypes = [POINTER(AtRenderSession), AtString, POINTER(c_float)]
AiRenderGetHintFlt.restype = c_bool

AiRenderGetHintStr = ai.AiRenderGetHintStr
AiRenderGetHintStr.argtypes = [POINTER(AtRenderSession), AtString, POINTER(AtString)]
AiRenderGetHintStr.restype = c_bool

AiRenderSetHintBool = ai.AiRenderSetHintBool
AiRenderSetHintBool.argtypes = [POINTER(AtRenderSession), AtString, c_bool]
AiRenderSetHintBool.restype = c_bool

AiRenderSetHintInt = ai.AiRenderSetHintInt
AiRenderSetHintInt.argtypes = [POINTER(AtRenderSession), AtString, c_int]
AiRenderSetHintInt.restype = c_bool

AiRenderSetHintFlt = ai.AiRenderSetHintFlt
AiRenderSetHintFlt.argtypes = [POINTER(AtRenderSession), AtString, c_float]
AiRenderSetHintFlt.restype = c_bool

AiRenderSetHintStr = ai.AiRenderSetHintStr
AiRenderSetHintStr.argtypes = [POINTER(AtRenderSession), AtString, AtString]
AiRenderSetHintStr.restype = c_bool

# It is preferred to create the callback and hold onto the reference to it for
# the lifetime of the render session:
#
#     def render_update(private_data, update_type, update_info):
#         ...
#     my_render_update_callback = arnold.AtRenderUpdateCallback(render_update)
#     arnold.AiRenderBegin(update_callback=my_render_update_callback)
#     ...
#     arnold.AiRenderEnd()
#
# It will also work to pass in a python function directly, although this will not
# work for multiple render sessions simultaneously, like the above method will.
def AiRenderBegin(render_session, mode = AI_RENDER_MODE_CAMERA, update_callback = None, private_data = None):
    func = ai.AiRenderBegin
    func.argtypes = [POINTER(AtRenderSession), AtRenderMode, AtRenderUpdateCallback, c_void_p]
    func.restype = AtRenderErrorCode

    cprivatedata = ctypes.cast(pointer(ctypes.py_object(private_data)), c_void_p)
    if update_callback is not None and type(update_callback) == AtRenderUpdateCallback:
        return func(render_session, mode, update_callback, cprivatedata)
    else:
        global cupdatecb
        cupdatecb = AtRenderUpdateCallback(update_callback if update_callback is not None else 0)
        return func(render_session, mode, cupdatecb, cprivatedata)

AiRenderEnd = ai.AiRenderEnd
AiRenderEnd.argtypes = [POINTER(AtRenderSession)]
AiRenderEnd.restype = AtRenderErrorCode

AiRenderGetStatus = ai.AiRenderGetStatus
AiRenderGetStatus.argtypes = [POINTER(AtRenderSession)]
AiRenderGetStatus.restype = AtRenderStatus

def AiRenderInterrupt(rs, blocking = AI_NON_BLOCKING):
    func = ai.AiRenderInterrupt
    func.argtypes = [POINTER(AtRenderSession), AtBlockingCall]
    func.restype = None
    func(rs, blocking)

def AiRenderAbort(rs, blocking = AI_NON_BLOCKING):
    func = ai.AiRenderAbort
    func.argtypes = [POINTER(AtRenderSession), AtBlockingCall]
    func.restype = None
    func(rs, blocking)

AiRenderResume = ai.AiRenderResume
AiRenderResume.argtypes = [POINTER(AtRenderSession)]
AiRenderResume.restype = None

AiRenderRestart = ai.AiRenderRestart
AiRenderRestart.argtypes = [POINTER(AtRenderSession)]
AiRenderRestart.restype = None

def AiRenderSession(universe, mode = AI_SESSION_BATCH):
    func = ai.AiRenderSession
    func.argtypes = [POINTER(AtUniverse), AtSessionMode]
    func.restype = POINTER(AtRenderSession)
    return NullToNone(func(universe, mode), POINTER(AtRenderSession))

def AiRenderSessionGetUniverse(rs):
    func = ai.AiRenderSessionGetUniverse
    func.argtypes = [POINTER(AtRenderSession)]
    func.restype = POINTER(AtUniverse)
    return NullToNone(func(rs), POINTER(AtUniverse))

def AiRenderSessionGetOptions(rs):
    func = ai.AiRenderSessionGetOptions
    func.argtypes = [POINTER(AtRenderSession)]
    func.restype = POINTER(AtNode)
    return NullToNone(func(rs), POINTER(AtNode))

def AiRenderSessionDestroy(rs):
    func = ai.AiRenderSessionDestroy
    func.argtypes = [POINTER(AtRenderSession)]
    func.restype = None
    func(rs)

def AiRenderIsAnyActive():
    func = ai.AiRenderIsAnyActive
    func.argtypes = []
    func.restype = c_bool
    return func()

def AiRender(render_session, render_mode = AI_RENDER_MODE_CAMERA):
    func = ai.AiRender
    func.argtypes = [POINTER(AtRenderSession), AtRenderMode]
    func.restype = AtRenderErrorCode
    return func(render_session, render_mode)
