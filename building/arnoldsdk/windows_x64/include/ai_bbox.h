// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Axis-aligned bounding box types and utilities.
 */

#pragma once
#include "ai_vector.h"
#include "ai_api.h"

#include <limits>

/** \defgroup ai_bbox AtBBox API
 * 
 * Bounding box creation and manipulation.
 * 
 * \details
 * The \ref AtBBox class is implemented as a 3D axis-aligned bounding box, using single
 * precision for its internal storage and operation.
 * 
 * \{
 */

/**
 * 3D axis-aligned bounding box (uses single-precision)
 */
struct AtBBox
{
   AtBBox() = default;

   AI_DEVICE AtBBox(const AtVector& mn, const AtVector& mx)
   {
      min = mn;
      max = mx;
   }

   /**
    * Compute the bbox of a triangle
    */
   AI_DEVICE AtBBox(const AtVector& p0, const AtVector& p1, const AtVector& p2)
   {
      min = max = p0;
      min = AiV3Min(min, p1);
      max = AiV3Max(max, p1);
      min = AiV3Min(min, p2);
      max = AiV3Max(max, p2);
   }

   /**
    * Expand a bounding box with some safety slack volume
    */
   AI_DEVICE void addSlack(float slack)
   {
      min -= slack;
      max += slack;
   }

   /**
    * Initialize a bounding box to be empty
    */
   void init()
   {
      const float bound = std::numeric_limits<float>::infinity();
      min = AtVector( bound,  bound,  bound);
      max = AtVector(-bound, -bound, -bound);
   }

   /**
    * Expand a bounding box with a point
    */
   void expand(const AtVector& v)
   {
      min = AiV3Min(min, v);
      max = AiV3Max(max, v);
   }

   /**
    * Check to see if the specified point is inside the bbox
    */
   AI_DEVICE bool inside(const AtVector& p) const
   {
      return AiAll(p >= min) && AiAll(p <= max);
   }

   /**
    * Compute the volume of a bbox
    */
   float volume() const
   {
      return (max.x - min.x) * (max.y - min.y) * (max.z - min.z);
   }

   /**
    * Returns whether or not the specified box is empty
    */
   bool isEmpty() const
   {
      return AiAny(min > max);
   }

   /**
    * Compute half the surface area of a bbox
    */
   float halfArea() const
   {
      const AtVector diag = max - min;
      return diag.x * (diag.y + diag.z) + diag.y * diag.z;
   }

   /**
    * Compute the surface area of a bbox
    */
   float area() const
   {
      return halfArea() * 2;
   }

   /**
    * Compute the center of a bbox
    */
   AI_DEVICE AtVector center() const
   {
      return (max + min) * 0.5f;
   }

   AtVector min, max;
};

/** 
 * Compute the "union" of two bboxes
 *
 * \note this name is misleading since it's the bbox of bboxes, not the
 * union (which can be disjoint)
 */
inline AtBBox AiBBoxUnion(const AtBBox& b1, const AtBBox& b2)
{
   return AtBBox(AiV3Min(b1.min, b2.min),
                 AiV3Max(b1.max, b2.max));
}

/** 
 * Compute the intersection of two bboxes
 */
inline AtBBox AiBBoxIntersection(const AtBBox& b1, const AtBBox& b2)
{
   return AtBBox(AiV3Max(b1.min, b2.min),
                 AiV3Min(b1.max, b2.max));
}

/**
 * Linear interpolation between two bboxes
 * (k=0 -> bbox=lo, k=1 -> bbox=hi) 
 */
inline AtBBox AiBBoxLerp(float k, const AtBBox& lo, const AtBBox& hi)
{
   return AtBBox(AiV3Lerp(k, lo.min, hi.min),
                 AiV3Lerp(k, lo.max, hi.max));
}

/** 
 * 2D axis-aligned bounding box (uses integers)
 */
struct AtBBox2
{
   AtBBox2() = default;

   constexpr AtBBox2(int min_x, int min_y, int max_x, int max_y) :
      minx(min_x), miny(min_y), maxx(max_x), maxy(max_y) {}

   /**
    * Compute the area (# of pixels) of an integer bbox
    */
   constexpr int AiBBox2Area() const
   {
      return (maxx - minx + 1) * (maxy - miny + 1);
   }

   int minx, miny, maxx, maxy;
};


/** \name Constants
 * \{
 */
static const AtBBox AI_BBOX_ZERO(AI_V3_ZERO, AI_V3_ZERO);
/*\}*/

/*\}*/
