# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

import os, sys, platform
import ctypes

class AtNode(ctypes.Structure):
    pass

def NullToNone(value, type):
    return ctypes.cast(value, type) if value else None

def _LoadArnold():
    libai = None

    OS = platform.system().lower()
    if not OS in ['windows', 'linux', 'darwin']:
        print(OS + ' not supported')
        return None
    if sys.maxsize <= 2**32:
        print('32 bit python not supported, must use 64 bit')
        return None
    ## Arnold library name
    ai_name = {
        'windows': 'ai.dll',
        'linux'  : 'libai.so',
        'darwin' : 'libai.dylib'
    }.get(OS)
    ## Arnold standard installation folder
    ai_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir, 'bin'))

    ld_path = os.environ.get({
        'windows': 'PATH',
        'linux'  : 'LD_LIBRARY_PATH',
        'darwin' : 'DYLD_LIBRARY_PATH'
    }.get(OS))

    ## Try to load Arnold from the system library path
    try:
        libai = ctypes.CDLL(ai_name)
        ## Check if it was loaded from a standard installation folder
        ## included in the system library path
        if ld_path:
            ld_path = map(lambda x: os.path.realpath(x), ld_path.split(os.pathsep))
            ai_ld_path = None
            for i in ld_path:
                if os.path.exists(os.path.join(i, ai_name)):
                    ai_ld_path = i
                    break
            if not ai_ld_path:
                print(ai_name + ' already loaded')
            elif ai_ld_path != ai_path:
                print(ai_name + ' loaded from non standard location ' + ai_ld_path)
        return libai
    except OSError:
        ## Try to load Arnold from the system library path again (explicitly adding each of the paths)
        ## NOTE: This is done since modifying an envvar within Python doesn't seem to affect the current process
        if ld_path:
            ld_path = map(lambda x: os.path.realpath(x), ld_path.split(os.pathsep))
            for p in ld_path:
                try:
                    libai = ctypes.CDLL(os.path.join(p, ai_name))
                    return libai
                except OSError:
                    pass

    ## Try to load Arnold from the standard installation folder
    try:
        if OS == 'windows':
            os.environ['PATH'] = ai_path + os.pathsep + os.environ['PATH']
            libai = ctypes.CDLL(ai_name)
        else:
            libai = ctypes.CDLL(os.path.join(ai_path, ai_name))
        return libai
    except OSError as err:
        print('Could not find ' + ai_name)
        print("OS error: {0}".format(err))

    return libai

ai = _LoadArnold()

if not ai:
    sys.exit(1)
