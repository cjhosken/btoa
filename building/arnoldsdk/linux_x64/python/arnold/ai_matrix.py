# Copyright 2020 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.

# TODO: Implement all matrix functions

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_vector import *

class AtMatrix(Structure):
    _fields_ = [("data", (c_float * 4) * 4)]

    def __init__(self, a1=0, a2=0, a3=0, a4=0, b1=0, b2=0, b3=0, b4=0, c1=0, c2=0, c3=0, c4=0, d1=0, d2=0, d3=0, d4=0):
        SM = c_float * 4
        a = SM(a1, a2, a3, a4)
        b = SM(b1, b2, b3, b4)
        c = SM(c1, c2, c3, c4)
        d = SM(d1, d2, d3, d4)
        MAT = SM * 4
        self.data = MAT(a, b, c, d)

    def __getitem__(self, index):
        return self.data[index]

AiM4Identity = ai.AiM4Identity
AiM4Identity.argtypes = []
AiM4Identity.restype = AtMatrix

AiM4IsIdentity = ai.AiM4IsIdentity
AiM4IsIdentity.argtypes = [POINTER(AtMatrix)]
AiM4IsIdentity.restype = c_bool

AiM4IsSingular = ai.AiM4IsSingular
AiM4IsSingular.argtypes = [POINTER(AtMatrix)]
AiM4IsSingular.restype = c_bool

AiM4PointByMatrixMult = ai.AiM4PointByMatrixMult
AiM4PointByMatrixMult.argtypes = [POINTER(AtMatrix), POINTER(AtVector)]
AiM4PointByMatrixMult.restype = AtVector

AiM4VectorByMatrixMult = ai.AiM4VectorByMatrixMult
AiM4VectorByMatrixMult.argtypes = [POINTER(AtMatrix), POINTER(AtVector)]
AiM4VectorByMatrixMult.restype = AtVector

AiM4Translation = ai.AiM4Translation
AiM4Translation.argtypes = [POINTER(AtVector)]
AiM4Translation.restype = AtMatrix

AiM4RotationX = ai.AiM4RotationX
AiM4RotationX.argtypes = [c_float]
AiM4RotationX.restype = AtMatrix

AiM4RotationY = ai.AiM4RotationY
AiM4RotationY.argtypes = [c_float]
AiM4RotationY.restype = AtMatrix

AiM4RotationZ = ai.AiM4RotationZ
AiM4RotationZ.argtypes = [c_float]
AiM4RotationZ.restype = AtMatrix

AiM4Scaling = ai.AiM4Scaling
AiM4Scaling.argtypes = [POINTER(AtVector)]
AiM4Scaling.restype = AtMatrix

AiM4Frame = ai.AiM4Frame
AiM4Frame.argtypes = [POINTER(AtVector), POINTER(AtVector), POINTER(AtVector), POINTER(AtVector)]
AiM4Frame.restype = AtMatrix

AiM4HPointByMatrixMult = ai.AiM4HPointByMatrixMult
AiM4HPointByMatrixMult.argtypes = [POINTER(AtMatrix), POINTER(AtHPoint)]
AiM4HPointByMatrixMult.restype = AtHPoint

AiM4VectorByMatrixTMult = ai.AiM4VectorByMatrixTMult
AiM4VectorByMatrixTMult.argtypes = [POINTER(AtMatrix), POINTER(AtVector)]
AiM4VectorByMatrixTMult.restype = AtVector

AiM4Mult = ai.AiM4Mult
AiM4Mult.argtypes = [POINTER(AtMatrix), POINTER(AtMatrix)]
AiM4Mult.restype = AtMatrix

AiM4Transpose = ai.AiM4Transpose
AiM4Transpose.argtypes = [POINTER(AtMatrix)]
AiM4Transpose.restype = AtMatrix

AiM4Invert = ai.AiM4Invert
AiM4Invert.argtypes = [POINTER(AtMatrix)]
AiM4Invert.restype = AtMatrix

AiM4Determinant = ai.AiM4Determinant
AiM4Determinant.argtypes = [POINTER(AtMatrix)]
AiM4Determinant.restype = c_double

AiM4Lerp = ai.AiM4Lerp
AiM4Lerp.argtypes = [c_float, POINTER(AtMatrix), POINTER(AtMatrix)]
AiM4Lerp.restype = AtMatrix
