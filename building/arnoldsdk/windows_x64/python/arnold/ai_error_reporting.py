# Copyright 2022 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai
from .ai_types import *

def AiErrorReportingSetEnabled(value) :
    func = ai.AiErrorReportingSetEnabled
    func.argtypes = [c_bool]
    func.restype = None
    func(value)

def AiErrorReportingGetEnabled() :
    func = ai.AiErrorReportingGetEnabled
    func.argtypes = []
    func.restype = c_bool
    return func()

def AiErrorReportingSetAutosendEmail(email) :
    func = ai.AiErrorReportingSetAutosendEmail
    func.argtypes = [AtString]
    func.restype = None
    func(email)

AiErrorReportingGetAutosendEmailFunc = ai.AiErrorReportingGetAutosendEmail
AiErrorReportingGetAutosendEmailFunc.argtypes = []
AiErrorReportingGetAutosendEmailFunc.restype = AtStringReturn

def AiErrorReportingGetAutosendEmail() :
    return AtStringToStr(AiErrorReportingGetAutosendEmailFunc())
