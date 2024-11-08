// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Shader globals struct, methods and macros
 */

#pragma once
#include "ai_params.h"
#include "ai_array.h"
#include "ai_color.h"
#include "ai_matrix.h"
#include "ai_vector.h"
#include "ai_string.h"
#include "ai_api.h"
#include <stdint.h> // uint32_t etc

// forward declarations
struct AtNode;
struct AtBucket;
struct AtLightSample;
struct AtShaderGlobalsPrivateInfo;

/** \defgroup ai_shader_globals  Shader Globals API
 * 
 * \ref AtShaderGlobals structure contains data accessible during the shading process.
 * 
 * \{
 */

/** Shader globals data structure
 *
 * \details
 * An AtShaderGlobals structure represents a \e shading \e context that holds
 * all the information accesible to the different types of shaders. For
 * example, after a camera ray hits the surface of an object, a shading
 * context of type \c AI_CONTEXT_SURFACE is created that contains, amongst
 * other things, local geometric properties such as the surface normal, the
 * UV surface parameters, etc.
 */
struct AtShaderGlobals {
   int32_t          x;                      /**< X raster-space coordinate of this ray tree                  */
   int32_t          y;                      /**< Y raster-space coordinate of this ray tree                  */
   float            px;                     /**< subpixel X coordinate of this ray in [0,1)                  */
   float            py;                     /**< subpixel Y coordinate of this ray in [0,1)                  */
   uint16_t         si;                     /**< subpixel sample index                                       */
   uint16_t         transp_index;           /**< transparency index                                          */
   AtVector         Ro;                     /**< ray origin (typically the camera position)                  */
   AtVector         Rd;                     /**< ray direction (normalized)                                  */
   float            Rl;                     /**< ray length (|Ro-P|)                                         */
   uint16_t         tid;                    /**< thread ID                                                   */
   uint8_t          Rt;                     /**< ray type                                                    */
   uint8_t          bounces;                /**< recursion level for the ray that created this hit           */
   uint8_t          bounces_diffuse;        /**< ray diffuse depth level                                     */
   uint8_t          bounces_specular;       /**< ray specular depth level                                    */
   uint8_t          bounces_reflect;        /**< ray reflection depth level                                  */
   uint8_t          bounces_transmit;       /**< ray transmission depth level                                */
   uint8_t          bounces_volume;         /**< ray volume depth level                                      */
   bool             fhemi;                  /**< force hemispherical lighting (use only upper hemisphere)    */
   float            time;                   /**< absolute time, between shutter-open and shutter-close       */
   AtNode*          Op;                     /**< pointer to the object being shaded                          */
   AtNode*          proc;                   /**< pointer to the procedural object (if exists)                */
   AtNode*          shader;                 /**< pointer to the current shader                               */
   const AtShaderGlobals* psg;              /**< parent shader globals (last shaded)                         */
   AtVector         Po;                     /**< shading point in object-space                               */
   AtVector         P;                      /**< shading point in world-space                                */
   AtVector         dPdx;                   /**< surface derivative wrt screen X-axis                        */
   AtVector         dPdy;                   /**< surface derivative wrt screen Y-axis                        */
   AtVector         N;                      /**< shading normal (in object space during displacement)        */
   AtVector         Nf;                     /**< face-forward shading normal                                 */
   AtVector         Ng;                     /**< geometric normal                                            */
   AtVector         Ngf;                    /**< face-forward geometric normal                               */
   AtVector         Ns;                     /**< smoothed normal (same as N but without bump)                */
   float            bu;                     /**< barycentric coordinate (aka alpha, or u)                    */
   float            bv;                     /**< barycentric coordinate (aka beta, or v)                     */
   float            u;                      /**< U surface parameter                                         */
   float            v;                      /**< V surface parameter                                         */
   uint32_t         fi;                     /**< primitive ID (triangle, curve segment, etc)                 */
   AtMatrix         M;                      /**< local-to-world matrix transform                             */
   AtMatrix         Minv;                   /**< world-to-local matrix transform                             */
   AtNode**         lights;                 /**< array of active lights at this shading context              */
   AtLightSample*   light_filter;           /**< light sample (for light filter shaders)                     */
   uint32_t         nlights;                /**< number of active lights at this shading context             */
   AtVector         dPdu;                   /**< surface derivative wrt U parameter                          */
   AtVector         dPdv;                   /**< surface derivative wrt V parameter                          */
   AtVector         dDdx;                   /**< ray direction derivative wrt screen X-axis                  */
   AtVector         dDdy;                   /**< ray direction derivative wrt screen Y-axis                  */
   AtVector         dNdx;                   /**< surface normal derivative wrt screen X-axis                 */
   AtVector         dNdy;                   /**< surface normal derivative wrt screen Y-axis                 */
   float            dudx;                   /**< U derivative wrt screen X-axis                              */
   float            dudy;                   /**< U derivative wrt screen Y-axis                              */
   float            dvdx;                   /**< V derivative wrt screen X-axis                              */
   float            dvdy;                   /**< V derivative wrt screen Y-axis                              */
   bool             skip_shadow;            /**< if true, don't trace shadow rays                            */
   uint8_t          sc;                     /**< type of shading context                                     */
   bool             inclusive_traceset;     /**< is the trace-set inclusive?                                 */
   AtString         traceset;               /**< trace-set to assign to rays made from this SG               */
   AtParamValue     out;                    /**< shader output                                               */

#ifdef AI_CPU_COMPILER
   AtShaderGlobalsPrivateInfo* privateinfo; /**< extra information for internal use                          */
   AI_DEVICE AtShaderGlobals() : privateinfo(NULL) {}
#else
   AtShaderGlobalsPrivateInfo* privateinfo =
      nullptr; /**< extra information for internal use                */
#endif
};

/** \name Shading Contexts
 *
 * \details
 * These macros let you determine the purpose that the shader globals were defined for.
 * \{
 */
#define AI_CONTEXT_SURFACE       0x00  /**< for ray-surface intersections           */
#define AI_CONTEXT_VOLUME        0x01  /**< for volume points during ray-marching   */
#define AI_CONTEXT_BACKGROUND    0x02  /**< for rays that don't hit any geometry    */
#define AI_CONTEXT_DISPLACEMENT  0x03  /**< for each vertex to be displaced         */
//#define AI_CONTEXT_INTERNAL    0x04  /**< reserved internal context; do not use   */
#define AI_CONTEXT_IMPORTANCE    0x05  /**< for importance sample table evaluations */
/* \}*/

AI_API AtShaderGlobals* AiShaderGlobals();
AI_API void             AiShaderGlobalsDestroy(AtShaderGlobals* sg);

/*\}*/
