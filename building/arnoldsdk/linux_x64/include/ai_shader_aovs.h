// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * AOV-writing functions for shaders
 */

#pragma once
#include "ai_api.h"
#include "ai_params.h"
#include "ai_color.h"
#include "ai_vector.h"
#include "ai_string.h"
#include <stdint.h> // uint32_t etc

struct AtShaderGlobals;

/** \defgroup ai_shader_aovs AOV (Arbitrary Output Variables) API 
 * \{
 *
 * AOV (Arbitrary Ouput Values) writing from inside a shader.
 * 
 * \details
 * Arnold can route any number of AOVs into any number of drivers that can
 * write to any number of output files.
 */

/** \name AOV-writing Functions
 *
 * \details
 * These functions allow the user to write AOVs.  Shaders may write
 * AOVs indiscriminately without hesitation because the system
 * understands the "context" in which an AOV write is performed. This means
 * Arnold can store AOVs when it "makes sense" and ignore writes when
 * it doesn't.
 *
 * For example, Arnold will not store "deep" AOV values (AOVs which are written 
 * at different depths for a singe pixel-sample) unless a driver specifically 
 * requests "deep" AOV values.  An example of a driver requiring "deep" AOV
 * values would be one which writes deep-texture/volume-shadow files.
 *
 * Arnold will only perform AOV writes from within the main
 * trunk of a pixel-sample ray-tree.  AOV writes made from inside a side-branch 
 * of the primary ray's ray-tree (such as a reflection) will be ignored.  Also,
 * AOV writes are ignored during shadow evaluations.
 *
 * \param sg    the current shader globals structure (pixel-sample state)
 * \param name  the name of the AOV to write into
 * \param val   the value to write into the AOV
 * \returns     a boolean indicating whether the write was successfully stored or not. 
 *              A failure could indicate that the AOV is not enabled, or is
 *              of the wrong type,  or is being written in the wrong "state" (such
 *              as not from within the trunk of the primary ray-tree).
 * \{
 */
AI_API AI_DEVICE bool AiAOVSetBool  (AtShaderGlobals* sg, const AtString name, bool      val);
AI_API AI_DEVICE bool AiAOVSetInt   (AtShaderGlobals* sg, const AtString name, int       val);
AI_API AI_DEVICE bool AiAOVSetFlt   (AtShaderGlobals* sg, const AtString name, float     val);
AI_API AI_DEVICE bool AiAOVSetRGB   (AtShaderGlobals* sg, const AtString name, AtRGB     val);
AI_API AI_DEVICE bool AiAOVSetRGBA  (AtShaderGlobals* sg, const AtString name, AtRGBA    val);
AI_API AI_DEVICE bool AiAOVSetVec   (AtShaderGlobals* sg, const AtString name, AtVector  val);
AI_API AI_DEVICE bool AiAOVSetVec2  (AtShaderGlobals* sg, const AtString name, AtVector2 val);
AI_API bool AiAOVSetMatrix(AtShaderGlobals* sg, const AtString name, AtMatrix  val);
AI_API AI_DEVICE bool AiAOVSetPtr   (AtShaderGlobals* sg, const AtString name, void*     val);
/*\}*/

/** \name AOV-reading Functions
 *
 * \details
 * These functions allow the user to read AOVs.
 *
 * \param sg    the current shader globals structure (pixel-sample state)
 * \param name  the name of the AOV to read from
 * \param val   the variable to store the read value
 * \returns     a boolean indicating whether the read was successfully done or not. 
 *              A failure could indicate that the AOV is not enabled, or is
 *              of the wrong type.
 * \{
 */
AI_API AI_DEVICE bool AiAOVGetBool  (const AtShaderGlobals* sg, const AtString name, bool&      val);
AI_API AI_DEVICE bool AiAOVGetInt   (const AtShaderGlobals* sg, const AtString name, int&       val);
AI_API AI_DEVICE bool AiAOVGetFlt   (const AtShaderGlobals* sg, const AtString name, float&     val);
AI_API AI_DEVICE bool AiAOVGetRGB   (const AtShaderGlobals* sg, const AtString name, AtRGB&     val);
AI_API AI_DEVICE bool AiAOVGetRGBA  (const AtShaderGlobals* sg, const AtString name, AtRGBA&    val);
AI_API AI_DEVICE bool AiAOVGetVec   (const AtShaderGlobals* sg, const AtString name, AtVector&  val);
AI_API AI_DEVICE bool AiAOVGetVec2  (const AtShaderGlobals* sg, const AtString name, AtVector2& val);
AI_API bool AiAOVGetMatrix(const AtShaderGlobals* sg, const AtString name, AtMatrix&  val);
AI_API AI_DEVICE bool AiAOVGetPtr   (const AtShaderGlobals* sg, const AtString name, void*&     val);
/*\}*/

#define AI_AOV_BLEND_NONE     0
#define AI_AOV_BLEND_OPACITY  1

AI_API bool AiAOVEnabled(const AtString name, uint8_t type);
AI_API bool AiAOVRegister(const char* name, uint8_t type, int blend_mode = AI_AOV_BLEND_NONE);

/*\}*/
