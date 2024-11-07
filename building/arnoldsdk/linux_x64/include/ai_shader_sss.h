// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * SSS functions for shaders
 */

#pragma once
#include "ai_color.h"

// forward declaration
struct AtShaderGlobals;

/** \defgroup ai_shader_sss Sub-Surface Scattering API
 * 
 * SSS utility functions.
 * 
 * \{
 */

AI_API         void  AiBSSRDFEmpirical(const AtShaderGlobals* sg, AtRGB& direct, AtRGB& indirect, const float* mfp, const float* albedo, const AtRGB* weight, unsigned int num = 1);
AI_API AI_PURE bool  AiShaderGlobalsFromSSS(const AtShaderGlobals* sg);

/*\}*/
