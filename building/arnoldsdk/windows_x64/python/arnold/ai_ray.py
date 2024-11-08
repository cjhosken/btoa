# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

from ctypes import *

# Ray Types
AI_RAY_UNDEFINED         = 0x00  # undefined type
AI_RAY_CAMERA            = 0x01  # ray originating at the camera
AI_RAY_SHADOW            = 0x02  # shadow ray towards a light source
AI_RAY_DIFFUSE_TRANSMIT  = 0x04  # indirect diffuse transmission ray
AI_RAY_SPECULAR_TRANSMIT = 0x08  # indirect specular transmission ray
AI_RAY_VOLUME            = 0x10  # indirect volume scattering ray
AI_RAY_DIFFUSE_REFLECT   = 0x20  # indirect diffuse reflection ray
AI_RAY_SPECULAR_REFLECT  = 0x40  # indirect specular reflection ray
AI_RAY_SUBSURFACE        = 0x80  # subsurface scattering probe ray

# Ray Type Masks
AI_RAY_ALL_DIFFUSE  = (0x04|0x20)  # all indirect diffuse ray types
AI_RAY_ALL_SPECULAR = (0x08|0x40)  # all indirect specular ray types
AI_RAY_ALL_REFLECT  = (0x20|0x40)  # all reflection ray types
AI_RAY_ALL_TRANSMIT = (0x04|0x08)  # all transmission specular ray types
AI_RAY_ALL          = 0xFF         # mask for all ray types
