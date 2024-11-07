// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Comparison
 */

#pragma once
#include "ai_api.h"

template<unsigned dim>
struct AtBooleanMask
{
   AI_DEVICE static AtBooleanMask<dim> lt(const float* x, const float* y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] < y[i];
      return r;
   }
   AI_DEVICE static AtBooleanMask<dim> le(const float* x, const float* y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] <= y[i];
      return r;
   }

   AI_DEVICE static AtBooleanMask<dim> gt(const float* x, const float* y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] > y[i];
      return r;
   }

   AI_DEVICE static AtBooleanMask<dim> ge(const float* x, const float* y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] >= y[i];
      return r;
   }


   AI_DEVICE static AtBooleanMask<dim> lt(const float* x, const float y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] < y;
      return r;
   }

   AI_DEVICE static AtBooleanMask<dim> le(const float* x, const float y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] <= y;
      return r;
   }

   AI_DEVICE static AtBooleanMask<dim> gt(const float* x, const float y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] > y;
      return r;
   }

   AI_DEVICE static AtBooleanMask<dim> ge(const float* x, const float y)
   {
      AtBooleanMask<dim> r;
      for (unsigned i=0; i < dim; ++i)
         r.data[i] = x[i] >= y;
      return r;
   }

   bool data[dim];
};

// some compilers (clang is fine, but at least icc 13 is not), aren't able to
// properly optimize with a for loop over the AtBooleanMask dim, so we have to
// do this manually
AI_DEVICE inline constexpr bool AiAny(const AtBooleanMask<2>& bm)
{
   return (bm.data[0] || bm.data[1]);
}

AI_DEVICE inline constexpr bool AiAll(const AtBooleanMask<2>& bm)
{
   return (bm.data[0] && bm.data[1]);
}

AI_DEVICE inline constexpr bool AiAny(const AtBooleanMask<3>& bm)
{
   return (bm.data[0] || bm.data[1] || bm.data[2]);
}

AI_DEVICE inline constexpr bool AiAll(const AtBooleanMask<3>& bm)
{
   return (bm.data[0] && bm.data[1] && bm.data[2]);
}

AI_DEVICE inline constexpr bool AiAny(const AtBooleanMask<4>& bm)
{
   return (bm.data[0] || bm.data[1] || bm.data[2] || bm.data[3]);
}

AI_DEVICE inline constexpr bool AiAll(const AtBooleanMask<4>& bm)
{
   return (bm.data[0] && bm.data[1] && bm.data[2] && bm.data[3]);
}
