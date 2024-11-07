// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Shader utilities for sampling direct lighting from light sources
 */

#pragma once
#include "ai_nodes.h"
#include "ai_shaderglobals.h"
#include "ai_color.h"
#include "ai_vector.h"
#include "ai_ray.h"

/** \defgroup ai_shader_lights Light Sampling API
 * 
 * Light sampling.
 * 
 * \{
 */

/** Light sample data structure */
struct AtLightSample {
   AI_DEVICE AtLightSample() :
      Lp             (NULL),
      Ldist          (0.f),
      Ld             (AI_V3_ZERO),
      Li             (AI_RGB_BLACK),
      Liu            (AI_RGB_BLACK),
      Lo             (AI_RGB_BLACK),
      pdf            (0.f),
      trace_ray_types(0) {}

   const AtNode*             Lp;              /**< pointer to light node                                               */
   float                     Ldist;           /**< distance from P to light source                                     */
   AtVector                  Ld;              /**< normalized direction vector from P to the light sample              */
   AtRGB                     Li;              /**< incident radiance, same as \c Liu * (1 - \c Lo)                     */
   AtRGB                     Liu;             /**< unoccluded incident radiance                                        */
   AtRGB                     Lo;              /**< shadow occlusion factor, (1,1,1) means fully occluded               */
   float                     pdf;             /**< sample probability density function                                 */
   uint8_t                   trace_ray_types; /**< bitmask of ray types that will return light hits from AiLightsTrace */
                                              /**< and so can use multiple importance sampling (MIS)                   */
};

/** \name Light Loop Methods
 * \details
 * This is the API for looping over light source samples.
 * \{
 */
AI_API void      AiLightsPrepare(AtShaderGlobals* sg);
AI_API bool      AiLightsGetSample(AtShaderGlobals* sg, AtLightSample& sample);
AI_API uint32_t  AiLightsTrace(AtShaderGlobals* sg, const AtVector& dir, uint8_t ray_type, AtLightSample*& hits);
AI_API uint8_t   AiLightsTraceRayTypes(AtShaderGlobals* sg);
AI_API void      AiLightsResetCache(AtShaderGlobals* sg);
AI_API AtRGB     AiLightsIntegrateShadowMatte(AtShaderGlobals* sg, AtBSDF *bsdf = NULL);
/*\}*/

/** \name Light Getter Methods
 * \details
 * These getters are to avoid slow AiNodeGet*() calls to access light parameters.
 * Only the most common attributes are exposed for now.
 * \{
 */
AI_API AI_PURE AtRGB AiLightGetColor(const AtNode* node);
AI_API AI_PURE float AiLightGetIntensity(const AtNode* node);
AI_API AI_PURE float AiLightGetDiffuse(const AtNode* node);
AI_API AI_PURE float AiLightGetSpecular(const AtNode* node);
AI_API AI_PURE float AiLightGetTransmission(const AtNode* node);
AI_API AI_PURE float AiLightGetSSS(const AtNode* node);
AI_API AI_PURE float AiLightGetVolume(const AtNode* node);
AI_API AI_PURE float AiLightGetInfluence(const AtShaderGlobals* sg, const AtNode* node, uint8_t ray_type);
/*\}*/

/** \name Light IES Format Parser
 * \details
 * Not a shader specific call, this is called by plugins or host DCCs to parse IES files
 * \{
 */

AI_API bool AiLightIESLoad(const AtString filename, const unsigned int width, const unsigned int height, float* max_intensity, float* data);

/*\}*/

/*\}*/
