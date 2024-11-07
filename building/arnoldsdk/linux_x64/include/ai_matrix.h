// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Matrix math type and methods
 */

#pragma once
#include "ai_vector.h"
#include "ai_api.h"
#include "ai_matrix_private.h"

#include <cstring>
#include <stdint.h>

/** \defgroup ai_matrix AtMatrix API
 * 
 * \ref AtMatrix type creation and operation.
 * 
 * \{
 */

#ifndef _ARNOLDDLL
// Visual Studio will report a compile error if AtMatrix is templated, so we use this
// one instead of the version in ai_matrix_private.h
struct AtMatrix {
   bool operator==(const AtMatrix& m) const
   {
      // watch out, this will return false for +0.0 == -0.0 and true for matching NaNs
      return !memcmp(data, m.data, sizeof(AtMatrix));
   }

   constexpr const float* operator[](int t) const
   {
      return (const float*) &(data[t][0]);
   }

   float* operator[](int t)
   {
      return &(data[t][0]);
   }

   float data[4][4];
};
#endif

AI_API AI_DEVICE AtMatrix AiM4Identity();
AI_API           AtMatrix AiM4Translation(const AtVector& t);
AI_API AI_DEVICE AtMatrix AiM4RotationX(float x);
AI_API AI_DEVICE AtMatrix AiM4RotationY(float y);
AI_API AI_DEVICE AtMatrix AiM4RotationZ(float z);
AI_API           AtMatrix AiM4Scaling(const AtVector& s);
AI_API AI_DEVICE AtMatrix AiM4Frame(const AtVector& o, const AtVector& u, const AtVector& v, const AtVector& w);
AI_API AI_DEVICE AtVector AiM4PointByMatrixMult(const AtMatrix& m, const AtVector& pin);
AI_API AI_DEVICE AtHPoint AiM4HPointByMatrixMult(const AtMatrix& m, const AtHPoint& pin);
AI_API AI_DEVICE AtVector AiM4VectorByMatrixMult(const AtMatrix& m, const AtVector& vin);
AI_API AI_DEVICE AtVector AiM4VectorByMatrixTMult(const AtMatrix& m, const AtVector& vin);
AI_API AI_DEVICE AtMatrix AiM4Mult(const AtMatrix& ma, const AtMatrix& mb);
AI_API AI_DEVICE AtMatrix AiM4Transpose(const AtMatrix& min);
AI_API AI_DEVICE AtMatrix AiM4Invert(const AtMatrix& min);
AI_API AI_PURE   float    AiM4Determinant(const AtMatrix& m);
AI_API AI_DEVICE AtMatrix AiM4Lerp(float t, const AtMatrix& ma, const AtMatrix& mb);
AI_API AI_PURE   bool     AiM4IsIdentity(const AtMatrix& m);
AI_API AI_PURE   bool     AiM4IsSingular(const AtMatrix& m);

static constexpr const AtMatrix AI_M4_IDENTITY = {{ {1, 0, 0, 0},
                                                    {0, 1, 0, 0},
                                                    {0, 0, 1, 0},
                                                    {0, 0, 0, 1} }};
static constexpr const AtMatrix AI_M4_ZERO =     {{ {0, 0, 0, 0},
                                                    {0, 0, 0, 0},
                                                    {0, 0, 0, 0},
                                                    {0, 0, 0, 0} }};

/*\}*/
