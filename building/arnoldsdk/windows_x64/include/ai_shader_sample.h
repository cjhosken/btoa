// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Struct returned by AiTrace(), called "screen sample" for legacy reasons
 */

#pragma once
#include "ai_color.h"
#include "ai_vector.h"

#ifdef AI_CPU_COMPILER
#include <stdint.h> // uint32_t etc
#endif

// forward declarations
struct AtNode;

/** \defgroup ai_shader_sample  Screen Sample
 * 
 * Definition of the \ref AtScrSample structure.
 * 
 * \{
 */

/** Used to hold the result of AiTrace() calls */
struct AtScrSample {
   AtRGB         color;    /**< color                  */
   AtRGB         opacity;  /**< opacity                */
   float         alpha;    /**< alpha                  */
   AtVector      point;    /**< 3D hit point           */
   uint32_t      face;     /**< triangle ID of hit     */
   const AtNode* obj;      /**< pointer to object hit  */
   float         z;        /**< hit distance (Z depth) */
};

/*\}*/
