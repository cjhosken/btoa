// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Radiance and irradiance lookup functions
 */

#pragma once
#include "ai_shaderglobals.h"

/** \defgroup ai_shader_radiance Irradiance / Radiance API
 * 
 * Radiance and irradiance lookup functions.
 * 
 * \{
 */       

AI_API AtRGB AiIrradiance(const AtVector& p, const AtVector& n, int tid, uint32_t pid);
AI_API AtRGB AiRadiance(const AtVector& p, const AtVector& dir, const AtVector& n, AtNode* obj, uint32_t face, float u, float v, AtNode* shader, int tid, uint32_t pid);

/*\}*/
