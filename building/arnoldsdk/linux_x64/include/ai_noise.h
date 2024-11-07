// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Perlin noise and Worley cellular noise, in both scalar and vector flavors
 */

#pragma once
#include "ai_vector.h"
#include "ai_api.h"

/** \defgroup ai_noise Procedural Texturing API
 * 
 * Multiple noise functions, in both scalar and vector flavors.
 * 
 * \{                                                                              
 */       

/** \name Perlin Noise
 * \{
 */
AI_API AI_DEVICE AI_CONST float AiPerlin2(AtVector2 p);
AI_API AI_DEVICE AI_CONST float AiPerlin3(AtVector p);
AI_API AI_DEVICE AI_CONST float AiPerlin4(AtVector p, float time);
/*\}*/

/** \name Periodic Perlin Noise
 * \{
 */
AI_API AI_DEVICE AI_CONST float AiPeriodicPerlin2(AtVector2 p, int periodx, int periody);
AI_API AI_DEVICE AI_CONST float AiPeriodicPerlin3(AtVector p, int periodx, int periody, int periodz);
AI_API AI_DEVICE AI_CONST float AiPeriodicPerlin4(AtVector p, float time, int periodx, int periody, int periodz, int periodt);
/*\}*/

/** \name Summed-Noise
 * \{
 */
AI_API AI_DEVICE AI_CONST float     AiNoise2 (AtVector2 p, int octaves, float distortion, float lacunarity);
AI_API AI_DEVICE AI_CONST float     AiNoise3 (AtVector p, int octaves, float distortion, float lacunarity);
AI_API AI_DEVICE AI_CONST float     AiNoise4 (AtVector p, float time, int octaves, float distortion, float lacunarity);
AI_API AI_DEVICE AI_CONST AtVector2 AiVNoise2(AtVector2 p, int octaves, float distortion, float lacunarity);
AI_API AI_DEVICE AI_CONST AtVector  AiVNoise3(AtVector p, int octaves, float distortion, float lacunarity);
AI_API AI_DEVICE AI_CONST AtVector  AiVNoise4(AtVector p, float time, int octaves, float distortion, float lacunarity);
/*\}*/

/** \name Cellular Noise
 * \{
 */
AI_API AI_DEVICE void               AiCellular(AtVector p, int n, int octaves, float lacunarity, float randomness, float* F, AtVector* delta = NULL, uint32_t* ID = NULL);
AI_API AI_DEVICE AI_CONST float     AiCellNoise2(AtVector2 p);
AI_API AI_DEVICE AI_CONST float     AiCellNoise3(AtVector p);
AI_API AI_DEVICE AI_CONST float     AiCellNoise4(AtVector p, float t);
AI_API AI_DEVICE AI_CONST AtVector2 AiVCellNoise2(AtVector2 p);
AI_API AI_DEVICE AI_CONST AtVector  AiVCellNoise3(AtVector p);
AI_API AI_DEVICE AI_CONST AtVector  AiVCellNoise4(AtVector p, float t);
/*\}*/

/*\}*/
