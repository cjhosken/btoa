# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *
from .arnold_common import ai

import platform
import sys
import ctypes

# for python 3, strings need to be converted to char pointers. we
# assume arnold takes utf-8 encoded strings 
if sys.version_info[0] >= 3:
    class AtPythonString(c_char_p):
        @classmethod
        def from_param(cls, obj):
            if (obj is not None) and (not isinstance(obj, cls)):
                if isinstance(obj, str):
                    obj = obj.encode('utf-8')
            return c_char_p.from_param(obj)

        def __str__(self):
            if self.value is None:
                    return ""
            return self.decode()
      
        def decode(self):
            if self.value is None:
                return None
            return self.value.decode('utf-8')
     
    def AtPythonStringToStr(astring):
        return str(astring)
else:
    AtPythonString = c_char_p

    def AtPythonStringToStr(string):
        return string

if sys.version_info[0] >= 3:
    class AtString(c_char_p):
        @classmethod
        def from_param(cls, obj):
            if (obj is not None) and (not isinstance(obj, cls)):
                if isinstance(obj, str):
                    obj = obj.encode('utf-8')
            return AtStringStruct(ai.AiCreateAtStringData_private(c_char_p(obj)))

        def __str__(self):
            if self.value is None:
                    return ""
            return self.decode()

        def decode(self):
            if self.value is None:
                return None
            return self.value.decode('utf-8')

    def AtStringToStr(astring):
        return str(astring)
else:
    class AtString(c_char_p):
        @classmethod
        def from_param(self, param):
            rs = AtStringStruct(ai.AiCreateAtStringData_private(c_char_p(param)))
            return rs

    def AtStringToStr(string):
        return str(string)

class AtStringStruct(ctypes.Structure):
    _fields_ = [("data", POINTER(c_char))]
    def __str__(self):
        if self.data is None:
            return ""
        length = ai.AiAtStringLength(self.data)
        if sys.version_info[0] >= 3:
            return self.data[:length].decode('utf-8')
        else:
            return self.data[:length]

# workaround calling convention mismatch, where structs with constructors that
# are 8 bytes or less and not too complex in other ways (see trac#5791)
# get stored by reference in registers while ctypes expects them by value
return_small_struct_exception = platform.system().lower() == 'windows'

if return_small_struct_exception:
    class AtStringReturn(ctypes.Structure):
        _fields_ = [("data", POINTER(c_char)),
                    ("workaround", c_char)]
        def __str__(self):
            if self.data is None:
                return ""
            length = ai.AiAtStringLength(self.data)
            if sys.version_info[0] >= 3:
                return self.data[:length].decode('utf-8')
            else:
                return self.data[:length]
else:
    AtStringReturn = AtStringStruct

ai.AiCreateAtStringData_private.argtypes = [AtPythonString]
ai.AiCreateAtStringData_private.restype  = POINTER(c_char)

AtBlockingCall = c_int
AI_BLOCKING     = AtBlockingCall(0)
AI_NON_BLOCKING = AtBlockingCall(1)
