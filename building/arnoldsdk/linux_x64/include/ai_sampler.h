// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * A generic, two-dimensional sampler that is sometimes useful when writing shaders
 */

#pragma once
#include "ai_api.h"
#include <stdint.h> // uint32_t etc

// forward declarations (defined elsewhere)
struct AtShaderGlobals;

/** \defgroup ai_sampler Sampler API
 * 
 * A generic, two-dimensional sampler that is sometimes useful when writing shaders.
 * 
 * \{
 */

/**
 * \struct AtSampler
 * Opaque data type for a sampler
 */
struct AtSampler;

/**
 * \struct AtSamplerIterator
 * Opaque data type for a sampler iterator
 */
struct AtSamplerIterator;

AI_API AtSampler*         AiSampler(uint32_t seed, int nsamples, int ndim);
AI_API AtSamplerIterator* AiSamplerIterator(const AtSampler* sampler, const AtShaderGlobals* sg);
AI_API AI_DEVICE bool     AiSamplerGetSample(AtSamplerIterator* iterator, float* sample);
AI_API AI_PURE int        AiSamplerGetSampleCount(const AtSamplerIterator* iterator);
AI_API AI_PURE float      AiSamplerGetSampleInvCount(const AtSamplerIterator* iterator);
AI_API void               AiSamplerDestroy(AtSampler* sampler);

/*\}*/
