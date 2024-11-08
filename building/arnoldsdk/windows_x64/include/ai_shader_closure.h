// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Shader closures
 */

#pragma once
#include "ai_closure.h"
#include "ai_color.h"
#include "ai_shaderglobals.h"

/** \defgroup ai_shader_closure Shader Closure API
 *
 *  \ref AtClosure creation. Shaders can return these instead of final colors.
 *
 *  \details
 *  Closures describe the way surfaces and volumes scatter light,
 *  leaving the lights loops and integration to Arnold.
 *
 *  For creating BSDF closures, an \c AtBSDF can be wrapped in a closure:
 *  \code
 *  AtBSDF *bsdf = AiOrenNayarBSDF(sg, sg->Nf);
 *  sg->out.CLOSURE() = AtClosure(diffuse_color, bsdf);
 *  \endcode
 *
 * \{
 */


/* BSSRDF random walk versions */
enum class AtRandomWalkVersion
{
   // This is a brute-force Monte Carlo random walk approach to subsurface scattering
   // that produces estimates from a series of simulated interior scattering events.
   v1 = 1,

   // This is an improved version of the brute-force Monte Carlo v1, that
   // suffers from less brightening and desaturation at corners. Please note that
   // this change causes light to penetrate more deeply at grazing angles, which
   // can cause an increase in noise and scattering distance.
   v2,

   // This version of the random walk SSS was designed for OpenPBR.
   v3
};

/* BSSRDF Closures */
AI_API AI_DEVICE AtClosure AiClosureEmpiricalBSSRDF(const AtShaderGlobals* sg, const AtRGB& weight, const AtVector& mfp, const AtRGB& albedo);

AI_API AI_DEVICE AtClosure AiClosureRandomWalkBSSRDF(const AtShaderGlobals* sg, const AtRandomWalkVersion& version,
                                                     const AtRGB& weight, const AtVector& mfp, const AtRGB& albedo, float g = 0.0f);

AI_API AI_DEVICE void AiClosureBSSRDFSetDirectIndirect(AtClosure closure, float weight_direct, float weight_indirect);

/* Emission Closures */
AI_API AI_DEVICE AtClosure AiClosureEmission(const AtShaderGlobals* sg, const AtRGB& weight);

/* Transparency & Matte Closures */
AI_API AI_DEVICE AtClosure AiClosureTransparent(const AtShaderGlobals* sg, const AtRGB& weight = AI_RGB_WHITE, const AtClosureList interior = NULL, int32_t importance=0);
AI_API AI_DEVICE AtClosure AiClosureMatte(const AtShaderGlobals* sg, const AtRGB& weight = AI_RGB_WHITE);

/* Background Closure */
AI_API AtClosure AiClosureBackground(const AtShaderGlobals* sg, const AtRGB& weight = AI_RGB_WHITE);

/* Volume Closures */
AI_API AI_DEVICE AtClosure AiClosureVolumeAbsorption(const AtShaderGlobals* sg, const AtRGB& weight);
AI_API AI_DEVICE AtClosure AiClosureVolumeEmission(const AtShaderGlobals* sg, const AtRGB& weight);
AI_API AI_DEVICE AtClosure AiClosureVolumeHenyeyGreenstein(const AtShaderGlobals* sg, const AtRGB& absorption, const AtRGB& scattering, const AtRGB& emission, float g = 0.f);
AI_API AI_DEVICE AtClosure AiClosureVolumeDoubleHenyeyGreenstein(const AtShaderGlobals* sg, const AtRGB& absorption, const AtRGB& scattering, const AtRGB& emission, float g = 0.f, float g2=0.f, float w2=0.f);

AI_API AI_DEVICE AtClosure AiClosureVolumeMatte(const AtShaderGlobals* sg, const AtRGB& weight);
AI_API AI_DEVICE AtClosure AiClosureVolumeAtmosphere(const AtShaderGlobals* sg, const AtRGB& emission, const AtRGB& transparent, const AtRGB& matte);

/*\}*/
