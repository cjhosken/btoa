// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Ray struct and various trace functions
 */

#pragma once
#include "ai_vector.h"
#include <stdint.h> // uint32_t etc
#include "ai_shader_sample.h"
#ifdef AI_CPU_COMPILER
#include "ai_string.h"
#include "ai_matrix.h"
#else
#include <ai_color.h>
#endif

// forward declaration
struct AtShaderGlobals;
struct AtLightSample;

/** \defgroup ai_ray Ray Tracing API
 * 
 * Creation and manipulation of \ref AtRay objects
 * 
 * \{
 */

/** \name Ray Types
 * \{
 */
#define AI_RAY_UNDEFINED         0x00  /**< undefined type                      */
#define AI_RAY_CAMERA            0x01  /**< ray originating at the camera       */
#define AI_RAY_SHADOW            0x02  /**< shadow ray towards a light source   */
#define AI_RAY_DIFFUSE_TRANSMIT  0x04  /**< indirect diffuse transmission ray   */
#define AI_RAY_SPECULAR_TRANSMIT 0x08  /**< indirect specular transmission ray  */
#define AI_RAY_VOLUME            0x10  /**< indirect volume scattering ray      */
#define AI_RAY_DIFFUSE_REFLECT   0x20  /**< indirect diffuse reflection ray     */
#define AI_RAY_SPECULAR_REFLECT  0x40  /**< indirect specular reflection ray    */
#define AI_RAY_SUBSURFACE        0x80  /**< subsurface scattering probe ray     */
/*\}*/

/** \name Ray Type Masks
 * \{
 */
#define AI_RAY_ALL_DIFFUSE  (AI_RAY_DIFFUSE_TRANSMIT | AI_RAY_DIFFUSE_REFLECT)   /**< all indirect diffuse ray types      */
#define AI_RAY_ALL_SPECULAR (AI_RAY_SPECULAR_TRANSMIT| AI_RAY_SPECULAR_REFLECT)  /**< all indirect specular ray types     */
#define AI_RAY_ALL_REFLECT  (AI_RAY_DIFFUSE_REFLECT  | AI_RAY_SPECULAR_REFLECT)  /**< all reflection ray types            */
#define AI_RAY_ALL_TRANSMIT (AI_RAY_DIFFUSE_TRANSMIT | AI_RAY_SPECULAR_TRANSMIT) /**< all transmission specular ray types */
#define AI_RAY_ALL          uint8_t(-1)                                          /**< mask for all ray types              */
/*\}*/

/** Ray data structure */
struct AtRay {
   uint8_t      type;                   /**< Type of ray (\c AI_RAY_CAMERA, etc)             */
   uint8_t      bounces;                /**< Number of bounces so far (0 for camera rays)    */
   uint8_t      bounces_diffuse;        /**< Number of diffuse bounces so far                */
   uint8_t      bounces_specular;       /**< Number of specular bounces so far               */
   uint8_t      bounces_reflect;        /**< Number of reflection bounces so far             */
   uint8_t      bounces_transmit;       /**< Number of transmission bounces so far           */
   uint8_t      bounces_volume;         /**< Number of volume bounces so far                 */
#ifdef AI_CPU_COMPILER
   bool         inclusive_traceset;     /**< Is the trace-set inclusive or exclusive?        */
   AtString     traceset;               /**< Trace-set for this ray                          */
   uint16_t     tid;                    /**< Thread ID                                       */
#endif
   uint16_t     sindex;                 /**< Sub-pixel sample index when supersampling       */
   int          x;                      /**< Raster-space X coordinate                       */
   int          y;                      /**< Raster-space Y coordinate                       */
   float        px;                     /**< Subpixel X coordinate in [0,1)                  */
   float        py;                     /**< Subpixel Y coordinate in [0,1)                  */
   AtVector     origin;                 /**< Ray origin                                      */
   AtVector     dir;                    /**< Unit ray direction                              */
   float        mindist;                /**< Minimum useful distance from the origin         */
   float        maxdist;                /**< Maximum useful distance from the origin (volatile while ray is traced) */
   const AtShaderGlobals* psg;          /**< Parent shader globals (last shaded)             */
   const AtLightSample* light_sample;   /**< Associated light sample, for shadow rays only   */
   AtRGB        weight;                 /**< Ray weight, AI_RGB_WHITE for clean camera rays  */
   float        time;                   /**< Time at which the ray was created, in [0,1)     */
   AtVector     dOdx;                   /**< Partial derivative of ray origin wrt image-space X coordinate    */
   AtVector     dOdy;                   /**< Partial derivative of ray origin wrt image-space Y coordinate    */
   AtVector     dDdx;                   /**< Partial derivative of ray direction wrt image-space X coordinate */
   AtVector     dDdy;                   /**< Partial derivative of ray direction wrt image-space Y coordinate */
};

AI_API AI_DEVICE AtRay AiMakeRay(uint8_t type, const AtVector& origin, const AtVector* dir, float maxdist, const AtShaderGlobals* sg);

#ifdef AI_CPU_COMPILER
AI_API void  AiReflectRay(AtRay& ray, const AtVector& normal, const AtShaderGlobals* sg);
#endif
AI_API AI_DEVICE bool  AiRefractRay(AtRay& ray, const AtVector& normal, float n1, float n2, const AtShaderGlobals* sg);
#ifdef AI_CPU_COMPILER
AI_API bool  AiTrace          (const AtRay& ray, const AtRGB& weight, AtScrSample& sample);
#endif
AI_API AI_DEVICE void  AiTraceBackground(const AtRay& ray, AtScrSample& sample);
#ifdef AI_CPU_COMPILER
AI_API bool  AiTraceProbe     (const AtRay& ray, AtShaderGlobals* sgout);
#endif

/*\}*/
