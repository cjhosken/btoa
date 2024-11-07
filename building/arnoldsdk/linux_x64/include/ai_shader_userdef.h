// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * User data functions for shaders
 */

#pragma once
#include "ai_shaderglobals.h"
#include "ai_array.h"
#include "ai_color.h"
#include "ai_matrix.h"
#include "ai_vector.h"
#include "ai_nodes.h"
#include "ai_string.h"
#include <stdint.h> // uint32_t etc

/** \defgroup ai_shader_userdef User-Data API
 *
 * User-defined data access on geometry.
 * 
 * \details
 * User-defined data (sometimes called "user-data") are new parameters that have 
 * been added to existing node-instances via AiNodeDeclare().
 *
 * There are four kinds of user-defined data: 
 *  - \c constant -- constant parameters are data that are defined on a per-object
 *                   basis and do not vary across the surface of that object.
 *  - \c uniform  -- uniform parameters are data that are defined on a "per-face"
 *                   basis.  During subdivision (if appropriate) values are
 *                   not interpolated.  Instead, the newly subdivided faces will
 *                   contain the value of their "parent" face.
 *  - \c varying  -- varying parameters are data that are defined on a per-vertex
 *                   basis.  During subdivision (if appropriate), the values 
 *                   at the new vertices are interpolated from the values at the
 *                   old vertices.  The user should only create parameters of
 *                   "interpolatable" variable types (such as floats, colors, etc.) 
 *  - \c indexed  -- indexed parameters are data that are defined on a per-face-vertex
 *                   basis.  During subdivision (if appropriate), the values
 *                   at the new vertices are interpolated from the values at the
 *                   old vertices, preserving edges where values were not shared.
 *                   The user should only create parameters of "interpolatable"
 *                   variable types (such as floats, colors, etc.)
 *
 * \{
 */


/** \name User-Data parameter
 *
 * \details
 * This macro is used to retrieve the user-data parameter from within the shaders.
 *
 * \param _name  a string with the name of the user-data value to query
 * \return       the parameter for the user data, or NULL if not found
 *
 * \{
 */
#define AiUDataGetParameter(_name) AiUserGetParameterFunc(_name, sg)
/*\}*/

/** \name User-Data Readers
 *
 * \details
 * These macros are used to retrieve user-data values from within
 * shaders.  If a varying-type user-data is requested, then the
 * user-data will be correctly interpolated across the face of the primitive.
 *
 * In the case of reading constant-type user-data, the usual node-parameter
 * reading functions, such as AiNodeGetInt(), may also be used.
 *
 * \param _name  a string with the name of the user-data value to read
 * \param _val   the value in which to store the contents of the read operation
 * \return a boolean indicating whether the operation was successful
 *
 * Please refer to ai_shader_userdef.h for a description of the userdef-data
 * reading functions called by these macros.
 *
 * \{
 */
#define AiUDataGetBool(_name,_val)    AiUserGetBoolFunc  (_name, sg, _val)
#define AiUDataGetByte(_name,_val)    AiUserGetByteFunc  (_name, sg, _val)
#define AiUDataGetInt(_name,_val)     AiUserGetIntFunc   (_name, sg, _val)
#define AiUDataGetUInt(_name,_val)    AiUserGetUIntFunc  (_name, sg, _val)
#define AiUDataGetFlt(_name,_val)     AiUserGetFltFunc   (_name, sg, _val)
#define AiUDataGetRGB(_name,_val)     AiUserGetRGBFunc   (_name, sg, _val)
#define AiUDataGetRGBA(_name,_val)    AiUserGetRGBAFunc  (_name, sg, _val)
#define AiUDataGetVec(_name,_val)     AiUserGetVecFunc   (_name, sg, _val)
#define AiUDataGetVec2(_name,_val)    AiUserGetVec2Func  (_name, sg, _val)
#define AiUDataGetStr(_name,_val)     AiUserGetStrFunc   (_name, sg, _val)
#define AiUDataGetPtr(_name,_val)     AiUserGetPtrFunc   (_name, sg, _val)
#define AiUDataGetNode(_name,_val)    AiUserGetNodeFunc  (_name, sg, _val)
#define AiUDataGetArray(_name,_val)   AiUserGetArrayFunc (_name, sg, _val)
#define AiUDataGetMatrix(_name,_val)  AiUserGetMatrixFunc(_name, sg, _val)
/*\}*/


/** \name User-Data Derivatives with respect to screen X and Y
 *
 * \details
 * These macros are used to retrieve user-data derivatives w.r.t. X and Y from
 * within shaders.  If a varying-type user-data is requested, then the
 * user-data derivatives will be correctly interpolated across the face of the
 * primitive.  These derivatives can be useful in determining filter sizes to
 * match pixel footprints, such as when texture mapping.
 *
 * In the case of reading constant-type user-data, the derivatives are zero.
 *
 * \param _name     a string with the name of the user-data value to read
 * \param _dx_val   the value in which to store the contents of the
 *                  computed derivatives with respect to the X pixel direction
 * \param _dy_val   the value in which to store the contents of the
 *                  computed derivatives with respect to the Y pixel direction
 * \return a boolean indicating whether the operation was successful
 *
 * Please refer to ai_shader_userdef.h for a description of the userdef-data
 * reading functions called by these macros.
 *
 * \{
 */
#define AiUDataGetDxyDerivativesFlt(_name,_dx_val,_dy_val)     AiUserGetDxyDerivativesFltFunc   (_name, sg, _dx_val, _dy_val)
#define AiUDataGetDxyDerivativesRGB(_name,_dx_val,_dy_val)     AiUserGetDxyDerivativesRGBFunc   (_name, sg, _dx_val, _dy_val)
#define AiUDataGetDxyDerivativesRGBA(_name,_dx_val,_dy_val)    AiUserGetDxyDerivativesRGBAFunc  (_name, sg, _dx_val, _dy_val)
#define AiUDataGetDxyDerivativesVec(_name,_dx_val,_dy_val)     AiUserGetDxyDerivativesVecFunc   (_name, sg, _dx_val, _dy_val)
#define AiUDataGetDxyDerivativesVec2(_name,_dx_val,_dy_val)    AiUserGetDxyDerivativesVec2Func  (_name, sg, _dx_val, _dy_val)
#define AiUDataGetDxyDerivativesArray(_name,_dx_val,_dy_val)   AiUserGetDxyDerivativesArrayFunc (_name, sg, _dx_val, _dy_val)
#define AiUDataGetDxyDerivativesMatrix(_name,_dx_val,_dy_val)  AiUserGetDxyDerivativesMatrixFunc(_name, sg, _dx_val, _dy_val)
/*\}*/


/*\}*/

AI_API AI_DEVICE const AtUserParamEntry* AiUserGetParameterFunc(const AtString, const AtShaderGlobals*);

AI_API AI_DEVICE bool AiUserGetBoolFunc  (const AtString, const AtShaderGlobals*, bool&);
AI_API AI_DEVICE bool AiUserGetByteFunc  (const AtString, const AtShaderGlobals*, uint8_t&);
AI_API AI_DEVICE bool AiUserGetIntFunc   (const AtString, const AtShaderGlobals*, int&);
AI_API AI_DEVICE bool AiUserGetUIntFunc  (const AtString, const AtShaderGlobals*, unsigned int&);
AI_API AI_DEVICE bool AiUserGetFltFunc   (const AtString, const AtShaderGlobals*, float&);
AI_API AI_DEVICE bool AiUserGetRGBFunc   (const AtString, const AtShaderGlobals*, AtRGB&);
AI_API AI_DEVICE bool AiUserGetRGBAFunc  (const AtString, const AtShaderGlobals*, AtRGBA&);
AI_API AI_DEVICE bool AiUserGetVecFunc   (const AtString, const AtShaderGlobals*, AtVector&);
AI_API AI_DEVICE bool AiUserGetVec2Func  (const AtString, const AtShaderGlobals*, AtVector2&);
AI_API AI_DEVICE bool AiUserGetStrFunc   (const AtString, const AtShaderGlobals*, AtString&);
AI_API AI_DEVICE bool AiUserGetPtrFunc   (const AtString, const AtShaderGlobals*, void*&);
AI_API AI_DEVICE bool AiUserGetNodeFunc  (const AtString, const AtShaderGlobals*, AtNode*&);
AI_API AI_DEVICE bool AiUserGetArrayFunc (const AtString, const AtShaderGlobals*, AtArray*&);
AI_API AI_DEVICE bool AiUserGetMatrixFunc(const AtString, const AtShaderGlobals*, AtMatrix&);

AI_API AI_DEVICE bool AiUserGetDxyDerivativesFltFunc    (const AtString, const AtShaderGlobals*, float&, float&);
AI_API AI_DEVICE bool AiUserGetDxyDerivativesRGBFunc    (const AtString, const AtShaderGlobals*, AtRGB&, AtRGB&);
AI_API AI_DEVICE bool AiUserGetDxyDerivativesRGBAFunc   (const AtString, const AtShaderGlobals*, AtRGBA&, AtRGBA&);
AI_API AI_DEVICE bool AiUserGetDxyDerivativesVecFunc    (const AtString, const AtShaderGlobals*, AtVector&, AtVector&);
AI_API AI_DEVICE bool AiUserGetDxyDerivativesVec2Func   (const AtString, const AtShaderGlobals*, AtVector2&, AtVector2&);
AI_API AI_DEVICE bool AiUserGetDxyDerivativesArrayFunc  (const AtString, const AtShaderGlobals*, AtArray*&, AtArray*&);
AI_API AI_DEVICE bool AiUserGetDxyDerivativesMatrixFunc (const AtString, const AtShaderGlobals*, AtMatrix&, AtMatrix&);
