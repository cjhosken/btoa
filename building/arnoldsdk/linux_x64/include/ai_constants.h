// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Various useful constants
 */

#pragma once

#include <cfloat>

/** \defgroup ai_constants Constants
 * 
 * Numerical contants used throughout the Arnold code.
 * 
 * \{
 */

/**
 * \name Numerical Constants
 * \{
 */
#define AI_PI              (3.1415926535897931f)   /**< pi                             */
#define AI_PITIMES2        (6.2831853071795862f)   /**< 2 * pi                         */
#define AI_PIOVER2         (1.5707963267948966f)   /**< pi / 2                         */
#define AI_ONEOVERPI       (0.3183098861837906f)   /**< 1 / pi                         */
#define AI_ONEOVER2PI      (0.1591549430918953f)   /**< 1 / 2pi                        */
#define AI_E               (2.7182818284590452f)   /**< e                              */
#define AI_LOG2E           (1.4426950408889634f)   /**< log_2(e)                       */
#define AI_LN2             (0.6931471805599453f)   /**< ln(2)                          */
#define AI_SQRT2           (1.4142135623730951f)   /**< sqrt(2)                        */
#define AI_SQRT3           (1.7320508075688772f)   /**< sqrt(3)                        */
#define AI_GOLDEN          (1.6180339887498948f)   /**< golden ratio                   */
#define AI_DTOR            (0.0174532925199433f)   /**< Degrees to Radians             */
#define AI_RTOD            (57.295779513082323f)   /**< Radians to Degrees             */

#define AI_EPSILON         (1.0e-4f)               /**< System epsilon value           */
#define AI_OPACITY_EPSILON (1.0e-6f)               /**< Lowest possible opacity value  */
#define AI_BIG             (1.0e12f)               /**< Big number                     */
#define AI_INFINITE        (1.0e30f)               /**< Convention for an "infinite" number */
#define AI_ALMOST_ONE      (1.0f - FLT_EPSILON/2)  /**< One bit less than 1.0f         */
/* \}*/

/*\}*/
