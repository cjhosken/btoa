# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *

class AtLicenseInfo(Structure):
    _fields_ = [("used", c_bool),
                ("name", c_char * 64),
                ("ver", c_char * 64),
                ("exp", c_char * 64),
                ("options", c_char * 64),
                ("count", c_int),
                ("current_inuse", c_int),
                ("current_resuse", c_int),
                ("hbased", c_int),
                ("hold", c_int),
                ("max_roam", c_int),
                ("max_share", c_int),
                ("min_remove", c_int),
                ("min_checkout", c_int),
                ("min_timeout", c_int),
                ("nres", c_int),
                ("num_roam_allowed", c_int),
                ("roaming", c_int),
                ("share", c_int),
                ("soft_limit", c_int),
                ("thisroam", c_int),
                ("timeout", c_int),
                ("tz", c_int),
                ("tokens", c_int),
                ("type", c_int),
                ("ubased", c_int)]

AI_LIC_SUCCESS            =  0 # no error
AI_LIC_ERROR_CANTCONNECT  =  1 # can't connect to any rlm server
AI_LIC_ERROR_INIT         =  2 # error on initialization
AI_LIC_ERROR_NOTFOUND     =  3 # no licenses found (expired or not loaded)
AI_LIC_ERROR_NOTAVAILABLE =  4 # no licenses available (all in use)
AI_LIC_ERROR              = -1 # generic license error

ai.AiLicenseGetInfo.argtypes = [POINTER(POINTER(AtLicenseInfo)), POINTER(c_uint)]
ai.AiLicenseGetInfo.restype = c_int

def AiLicenseGetInfo(licenses, n):
    return ai.AiLicenseGetInfo(byref(licenses), byref(n))

AiLicenseIsAvailable = ai.AiLicenseIsAvailable
AiLicenseIsAvailable.argtypes = []
AiLicenseIsAvailable.restype = c_bool
