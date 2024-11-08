// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * This is enabled only inside of arnold and is disabled for client code.
 */
#pragma once
#include <cstring>
#include <stdint.h>

#ifdef _ARNOLDDLL
template <uint8_t ROWS, uint8_t COLS, typename T = float>
struct AtMatrixBase
{
   AI_DEVICE constexpr bool operator==(const AtMatrixBase& m) const
   {
      // watch out, this will return false for +0.0 == -0.0 and true for matching NaNs
      return !memcmp(data, m.data, sizeof(AtMatrixBase));
   }

   AI_DEVICE constexpr bool operator!=(const AtMatrixBase& m) const
   {
      return !(*this == m);
   }

   AI_DEVICE constexpr const T* operator[](int t) const
   {
      return (const T*) &(data[t][0]);
   }

   AI_DEVICE T* operator[](int t)
   {
      return &(data[t][0]);
   }

   T data[ROWS][COLS];
};

/* 4-by-4 matrix of floats */
using AtMatrix = AtMatrixBase<4, 4, float>;
#endif
