// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Volume functions for shaders
 */
 
#pragma once
#include "ai_color.h"
#include "ai_vector.h"
#include "ai_api.h"
#include "ai_string.h"

// forward declaration
struct AtShaderGlobals;

/** \defgroup ai_shader_volume Volume Rendering API
 * 
 * Volume functions for shaders.
 * 
 * \{
 */

/** \name Volume sampling
 *
 * \details
 * These macros are used to retrieve volume channel values from within
 * volume shaders.
 * 
 * \param      _channel  Name of data channel in the volume node
 * \param      _interp   Volume interpolation quality, one of \c AI_VOLUME_INTERP_*
 * \param[out] _val      Resulting sampled value at the shader globals position
 * \return               True if sampling was successful
 *
 * Please refer to ai_shader_volume.h for a description of the volume sampling
 * functions called by these macros.
 *
 * \{
 */
#define AiVolumeSampleFlt(_channel,_interp,_val)   AiVolumeSampleFltFunc (_channel, sg, _interp, _val)
#define AiVolumeSampleRGB(_channel,_interp,_val)   AiVolumeSampleRGBFunc (_channel, sg, _interp, _val)
#define AiVolumeSampleRGBA(_channel,_interp,_val)  AiVolumeSampleRGBAFunc(_channel, sg, _interp, _val)
#define AiVolumeSampleVec(_channel,_interp,_val)   AiVolumeSampleVecFunc (_channel, sg, _interp, _val)
#define AiVolumeSampleVec2(_channel,_interp,_val)  AiVolumeSampleVec2Func(_channel, sg, _interp, _val)
/*\}*/

AI_API AI_DEVICE bool AiVolumeSampleFltFunc (const AtString channel, const AtShaderGlobals *sg, int interp, float*    value);
AI_API AI_DEVICE bool AiVolumeSampleRGBFunc (const AtString channel, const AtShaderGlobals *sg, int interp, AtRGB*    value);
AI_API AI_DEVICE bool AiVolumeSampleRGBAFunc(const AtString channel, const AtShaderGlobals *sg, int interp, AtRGBA*   value);
AI_API AI_DEVICE bool AiVolumeSampleVecFunc (const AtString channel, const AtShaderGlobals *sg, int interp, AtVector* value);
AI_API AI_DEVICE bool AiVolumeSampleVec2Func(const AtString channel, const AtShaderGlobals *sg, int interp, AtVector2* value);

/*\}*/
